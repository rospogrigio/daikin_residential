"""Support for the Daikin HVAC."""
import logging

import voluptuous as vol

from homeassistant.components.climate import PLATFORM_SCHEMA, ClimateEntity
from homeassistant.components.climate.const import (
    ATTR_FAN_MODE,
    ATTR_HVAC_MODE,
    ATTR_PRESET_MODE,
    ATTR_SWING_MODE,
    HVAC_MODE_COOL,
    HVAC_MODE_DRY,
    HVAC_MODE_FAN_ONLY,
    HVAC_MODE_HEAT,
    HVAC_MODE_HEAT_COOL,
    HVAC_MODE_OFF,
    PRESET_AWAY,
    PRESET_COMFORT,
    PRESET_BOOST,
    PRESET_ECO,
    PRESET_NONE,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_FAN_MODE,
    SUPPORT_PRESET_MODE,
    SUPPORT_SWING_MODE,
)
from homeassistant.const import ATTR_TEMPERATURE, CONF_HOST, CONF_NAME, TEMP_CELSIUS
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN as DAIKIN_DOMAIN,
    DAIKIN_DEVICES,
    ATTR_INSIDE_TEMPERATURE,
    ATTR_OUTSIDE_TEMPERATURE,
    ATTR_ON_OFF,
    ATTR_STATE_OFF,
    ATTR_STATE_ON,
    ATTR_TARGET_TEMPERATURE,
)

_LOGGER = logging.getLogger(__name__)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {vol.Required(CONF_HOST): cv.string, vol.Optional(CONF_NAME): cv.string}
)


PRESET_MODES = {PRESET_BOOST, PRESET_COMFORT, PRESET_ECO, PRESET_AWAY}

HA_HVAC_TO_DAIKIN = {
    HVAC_MODE_FAN_ONLY: "fanOnly",
    HVAC_MODE_DRY: "dry",
    HVAC_MODE_COOL: "cooling",
    HVAC_MODE_HEAT: "heating",
    HVAC_MODE_HEAT_COOL: "auto",
    HVAC_MODE_OFF: "off",
}


HA_ATTR_TO_DAIKIN = {
    ATTR_PRESET_MODE: "en_hol",
    ATTR_HVAC_MODE: "mode",
    ATTR_FAN_MODE: "f_rate",
    ATTR_SWING_MODE: "f_dir",
    ATTR_INSIDE_TEMPERATURE: "htemp",
    ATTR_OUTSIDE_TEMPERATURE: "otemp",
    ATTR_TARGET_TEMPERATURE: "stemp",
}

DAIKIN_ATTR_ADVANCED = "adv"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old way of setting up the Daikin HVAC platform.

    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Daikin climate based on config_entry."""
    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():
        async_add_entities([DaikinClimate(device)], update_before_add=True)
    # daikin_api = hass.data[DAIKIN_DOMAIN].get(entry.entry_id)
    # async_add_entities([DaikinClimate(daikin_api)], update_before_add=True)


class DaikinClimate(ClimateEntity):
    """Representation of a Daikin HVAC."""

    def __init__(self, device):
        """Initialize the climate device."""

        self._device = device
        self._list = {
            ATTR_HVAC_MODE: list(HA_HVAC_TO_DAIKIN),
            ATTR_SWING_MODE: self._device.swing_modes,
        }

        self._supported_features = SUPPORT_TARGET_TEMPERATURE

        self._supported_preset_modes = [PRESET_NONE]
        self._current_preset_mode = PRESET_NONE
        for mode in PRESET_MODES:
            if self._device.support_preset_mode(mode):
                self._supported_preset_modes.append(mode)
                self._supported_features |= SUPPORT_PRESET_MODE

        if self._device.support_fan_rate:
            self._supported_features |= SUPPORT_FAN_MODE

        if self._device.support_swing_mode:
            self._supported_features |= SUPPORT_SWING_MODE

    async def _set(self, settings):
        """Set device settings using API."""
        values = {}

        for attr in [ATTR_TEMPERATURE, ATTR_FAN_MODE, ATTR_SWING_MODE, ATTR_HVAC_MODE]:
            value = settings.get(attr)
            if value is None:
                continue

            daikin_attr = HA_ATTR_TO_DAIKIN.get(attr)
            if daikin_attr is not None:
                if attr == ATTR_HVAC_MODE:
                    values[daikin_attr] = HA_HVAC_TO_DAIKIN[value]
                elif value in self._list[attr]:
                    values[daikin_attr] = value.lower()
                else:
                    _LOGGER.error("Invalid value %s for %s", attr, value)

            # temperature
            elif attr == ATTR_TEMPERATURE:
                try:
                    values[HA_ATTR_TO_DAIKIN[ATTR_TARGET_TEMPERATURE]] = str(int(value))
                except ValueError:
                    _LOGGER.error("Invalid temperature %s", value)

        if values:
            await self._device.set(values)

    @property
    def available(self):
        """Return the availability of the underlying device."""
        return self._device.available

    @property
    def supported_features(self):
        """Return the list of supported features."""
        return self._supported_features

    @property
    def name(self):
        """Return the name of the thermostat, if any."""
        return self._device.name

    @property
    def unique_id(self):
        """Return a unique ID."""
        devID = self._device.getId()
        return f"{devID}"

    @property
    def temperature_unit(self):
        """Return the unit of measurement which this thermostat uses."""
        return TEMP_CELSIUS

    @property
    def current_temperature(self):
        """Return the current temperature."""
        return self._device.inside_temperature

    @property
    def target_temperature(self):
        """Return the temperature we try to reach."""
        return self._device.target_temperature

    @property
    def max_temp(self):
        """Return the maximum temperature we are allowed to set."""
        return self._device.max_temp

    @property
    def min_temp(self):
        """Return the minimum temperature we are allowed to set."""
        return self._device.min_temp

    @property
    def target_temperature_step(self):
        """Return the supported step of target temperature."""
        stepVal = self._device.target_temperature_step
        return stepVal

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        # The service climate.set_temperature can set the hvac_mode too, see
        # https://www.home-assistant.io/integrations/climate/#service-climateset_temperature
        # se we first set the hvac_mode, if provided, then the temperature.
        if ATTR_HVAC_MODE in kwargs:
            await self.async_set_hvac_mode(kwargs[ATTR_HVAC_MODE])

        await self._device.async_set_temperature(kwargs[ATTR_TEMPERATURE])

    @property
    def hvac_mode(self):
        """Return current operation ie. heat, cool, idle."""
        return self._device.hvac_mode

    @property
    def hvac_modes(self):
        """Return the list of available operation modes."""
        return self._device.hvac_modes

    async def async_set_hvac_mode(self, hvac_mode):
        """Set HVAC mode."""
        await self._device.async_set_hvac_mode(HA_HVAC_TO_DAIKIN[hvac_mode])

    @property
    def fan_mode(self):
        """Return the fan setting."""
        return self._device.fan_mode

    @property
    def fan_modes(self):
        """List of available fan modes."""
        return self._device.fan_modes

    async def async_set_fan_mode(self, fan_mode):
        """Set new fan mode."""
        await self._device.async_set_fan_mode(fan_mode)

    @property
    def swing_mode(self):
        """Return the swing setting."""
        return self._device.swing_mode

    @property
    def swing_modes(self):
        """List of available swing modes."""
        return self._device.swing_modes

    async def async_set_swing_mode(self, swing_mode):
        """Set new swing mode."""
        await self._device.async_set_swing_mode(swing_mode)

    @property
    def preset_mode(self):
        """Return the preset_mode."""
        self._current_preset_mode = PRESET_NONE
        for mode in self._supported_preset_modes:
            if self._device.preset_mode_status(mode) == ATTR_STATE_ON:
                self._current_preset_mode = mode
        return self._current_preset_mode

    async def async_set_preset_mode(self, preset_mode):
        """Set preset mode."""
        curr_mode = self.preset_mode
        if curr_mode != PRESET_NONE:
            await self._device.set_preset_mode_status(curr_mode, ATTR_STATE_OFF)
        if preset_mode != PRESET_NONE:
            await self._device.set_preset_mode_status(preset_mode, ATTR_STATE_ON)

    @property
    def preset_modes(self):
        """List of available preset modes."""
        return self._supported_preset_modes

    async def async_update(self):
        """Retrieve latest state."""
        await self._device.api.async_update()

    async def async_turn_on(self):
        """Turn device on."""
        await self._device.setValue(ATTR_ON_OFF, ATTR_STATE_ON)

    async def async_turn_off(self):
        """Turn device off."""
        await self._device.setValue(ATTR_ON_OFF, ATTR_STATE_OFF)

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return self._device.device_info()
