"""Support for Daikin AirBase zones."""
from homeassistant.helpers.entity import ToggleEntity

from .daikin_base import Appliance

from .const import (
    DOMAIN as DAIKIN_DOMAIN,
    DAIKIN_DEVICES,
    ATTR_STATE_OFF,
    ATTR_STATE_ON,
    PRESET_STREAMER,
)

SWITCH_ICON = "hass:air-filter"


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Old way of setting up the platform.

    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Daikin climate based on config_entry."""
    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():
        switches = [PRESET_STREAMER]
        if device.support_preset_mode(PRESET_STREAMER):
            async_add_entities([DaikinSwitch(device, switch) for switch in switches])


class DaikinSwitch(ToggleEntity):
    """Representation of a switch."""

    def __init__(self, device: Appliance, switch_id: str):
        """Initialize the zone."""
        self._device = device
        self._switch_id = switch_id
        self._name = f"{device.name} {switch_id}"

    @property
    def unique_id(self):
        """Return a unique ID."""
        devID = self._device.getId()
        return f"{devID}-{self._switch_id}"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return SWITCH_ICON

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._device.preset_mode_status(self._switch_id) == ATTR_STATE_ON

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return self._device.device_info()

    async def async_update(self):
        """Retrieve latest state."""
        await self._device.api.async_update()

    async def async_turn_on(self, **kwargs):
        """Turn the zone on."""
        await self._device.set_preset_mode_status(self._switch_id, ATTR_STATE_ON)

    async def async_turn_off(self, **kwargs):
        """Turn the zone off."""
        await self._device.set_preset_mode_status(self._switch_id, ATTR_STATE_OFF)
