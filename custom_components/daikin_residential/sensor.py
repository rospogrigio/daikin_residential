"""Support for Daikin AC sensors."""
import logging

from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_ICON,
    CONF_NAME,
    CONF_TYPE,
    CONF_UNIT_OF_MEASUREMENT,
)
from homeassistant.components.sensor import (
    SensorEntity,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
)

from homeassistant.helpers.entity import EntityCategory

from .daikin_base import Appliance

from .const import (
    DOMAIN as DAIKIN_DOMAIN,
    DAIKIN_DEVICES,
    ATTR_COOL_ENERGY,
    ATTR_HEAT_ENERGY,
    ATTR_INSIDE_TEMPERATURE,
    ATTR_OUTSIDE_TEMPERATURE,
    ATTR_WIFI_STRENGTH,
    ATTR_WIFI_SSID,
    ATTR_LOCAL_SSID,
    ATTR_MAC_ADDRESS,
    ATTR_SERIAL_NUMBER,
    SENSOR_TYPE_ENERGY,
    SENSOR_TYPE_HUMIDITY,
    SENSOR_TYPE_POWER,
    SENSOR_TYPE_TEMPERATURE,
    SENSOR_TYPE_NETWORK_DIAGNOSTIC,
    SENSOR_PERIODS,
    SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, async_add_entities):
    """Old way of setting up the Daikin sensors.

    Can only be called when a user accidentally mentions the platform in their
    config. But even in that case it would have been ignored.
    """


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Daikin climate based on config_entry."""
    sensors = []
    for dev_id, device in hass.data[DAIKIN_DOMAIN][DAIKIN_DEVICES].items():
        if device.support_inside_temperature:
            _LOGGER.debug("device %s supports inside temperature", device.name)
            sensor = DaikinSensor.factory(device, ATTR_INSIDE_TEMPERATURE)
            sensors.append(sensor)
        if device.support_outside_temperature:
            _LOGGER.debug("device %s supports outside temperature", device.name)
            sensor = DaikinSensor.factory(device, ATTR_OUTSIDE_TEMPERATURE)
            sensors.append(sensor)
        if device.support_energy_consumption:
            _LOGGER.debug("device %s supports energy consumption", device.name)
            for period in SENSOR_PERIODS:
                sensor = DaikinSensor.factory(device, ATTR_COOL_ENERGY, period)
                sensors.append(sensor)
                sensor = DaikinSensor.factory(device, ATTR_HEAT_ENERGY, period)
                sensors.append(sensor)
        if device.support_wifi_strength:
            _LOGGER.debug("device %s supports wifi signal strength", device.name)
            sensor = DaikinSensor.factory(device, ATTR_WIFI_STRENGTH)
            sensors.append(sensor)
        if device.support_wifi_ssid:
            _LOGGER.debug("device %s supports wifi ssid", device.name)
            sensor = DaikinSensor.factory(device, ATTR_WIFI_SSID)
            sensors.append(sensor)
        if device.support_local_ssid:
            _LOGGER.debug("device %s supports local ssid", device.name)
            sensor = DaikinSensor.factory(device, ATTR_LOCAL_SSID)
            sensors.append(sensor)
        if device.support_mac_address:
            _LOGGER.debug("device %s supports mac address", device.name)
            sensor = DaikinSensor.factory(device, ATTR_MAC_ADDRESS)
            sensors.append(sensor)
        if device.support_serial_number:
            _LOGGER.debug("device %s supports serial number", device.name)
            sensor = DaikinSensor.factory(device, ATTR_SERIAL_NUMBER)
            sensors.append(sensor)
    async_add_entities(sensors)


class DaikinSensor(SensorEntity):
    """Representation of a Sensor."""

    @staticmethod
    def factory(device: Appliance, monitored_state: str, period=""):
        """Initialize any DaikinSensor."""
        cls = {
            SENSOR_TYPE_TEMPERATURE: DaikinClimateSensor,
            SENSOR_TYPE_HUMIDITY: DaikinClimateSensor,
            SENSOR_TYPE_POWER: DaikinEnergySensor,
            SENSOR_TYPE_ENERGY: DaikinEnergySensor,
            SENSOR_TYPE_NETWORK_DIAGNOSTIC: DaikinWiFiSensor,
        }[SENSOR_TYPES[monitored_state][CONF_TYPE]]
        return cls(device, monitored_state, period)

    def __init__(self, device: Appliance, monitored_state: str, period="") -> None:
        """Initialize the sensor."""
        self._device = device
        self._sensor = SENSOR_TYPES[monitored_state]
        self._period = period
        if period != "":
            periodName = SENSOR_PERIODS[period]
            self._name = f"{device.name} {periodName} {self._sensor[CONF_NAME]}"
        else:
            self._name = f"{device.name} {self._sensor[CONF_NAME]}"
        self._device_attribute = monitored_state

    @property
    def available(self):
        """Return the availability of the underlying device."""
        return self._device.available

    @property
    def unique_id(self):
        """Return a unique ID."""
        devID = self._device.getId()
        if self._period != "":
            return f"{devID}_{self._device_attribute}_{self._period}"
        return f"{devID}_{self._device_attribute}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        raise NotImplementedError

    @property
    def device_class(self):
        """Return the class of this device."""
        return self._sensor.get(CONF_DEVICE_CLASS)

    @property
    def icon(self):
        """Return the icon of this device."""
        return self._sensor.get(CONF_ICON)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._sensor[CONF_UNIT_OF_MEASUREMENT]

    async def async_update(self):
        """Retrieve latest state."""
        await self._device.api.async_update()

    @property
    def device_info(self):
        """Return a device description for device registry."""
        return self._device.device_info()


class DaikinClimateSensor(DaikinSensor):
    """Representation of a Climate Sensor."""

    @property
    def state(self):
        """Return the internal state of the sensor."""
        if self._device_attribute == ATTR_INSIDE_TEMPERATURE:
            return self._device.inside_temperature
        if self._device_attribute == ATTR_OUTSIDE_TEMPERATURE:
            return self._device.outside_temperature
        return None

    @property
    def state_class(self):
        return STATE_CLASS_MEASUREMENT


class DaikinEnergySensor(DaikinSensor):
    """Representation of a power/energy consumption sensor."""

    @property
    def state(self):
        """Return the state of the sensor."""
        if self._device_attribute == ATTR_COOL_ENERGY:
            return round(self._device.energy_consumption("cooling", self._period), 3)
        if self._device_attribute == ATTR_HEAT_ENERGY:
            return round(self._device.energy_consumption("heating", self._period), 3)
        return None

    @property
    def state_class(self):
        return STATE_CLASS_TOTAL_INCREASING


class DaikinWiFiSensor(DaikinSensor):
    """Representation of a WiFi Sensor."""
    
    # set default category for these entities
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    
    # auto disable these entities when added for the first time
    _attr_entity_registry_enabled_default = False

    @property
    def state(self):
        """Return the internal state of the sensor."""
        if self._device_attribute == ATTR_WIFI_STRENGTH:
            return self._device.wifi_strength
        if self._device_attribute == ATTR_WIFI_SSID:
            return self._device.wifi_ssid
        if self._device_attribute == ATTR_LOCAL_SSID:
            return self._device.local_ssid
        if self._device_attribute == ATTR_MAC_ADDRESS:
            return self._device.mac_address
        if self._device_attribute == ATTR_SERIAL_NUMBER:
            return self._device.serial_number
        return None

    @property
    def state_class(self):
        if self._device_attribute == ATTR_WIFI_STRENGTH:
            return STATE_CLASS_MEASUREMENT
        else:
            return None
