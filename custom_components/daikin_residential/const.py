"""Constants for Daikin Residential Controller."""

from homeassistant.const import (
    CONF_DEVICE_CLASS,
    CONF_TOKEN,
    CONF_ICON,
    CONF_NAME,
    CONF_TYPE,
    CONF_UNIT_OF_MEASUREMENT,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_SIGNAL_STRENGTH,
    ENERGY_KILO_WATT_HOUR,
    TEMP_CELSIUS,
    PERCENTAGE,
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
)

DOMAIN = "daikin_residential"

CONF_TOKENSET = CONF_TOKEN + "set"

DAIKIN_DATA = "daikin_data"
DAIKIN_API = "daikin_api"
DAIKIN_DEVICES = "daikin_devices"
DAIKIN_DISCOVERY_NEW = "daikin_discovery_new_{}"

ATTR_ON_OFF = "on_off"
ATTR_PRESET_MODE = "preset_mode"
ATTR_OPERATION_MODE = "operation_mode"
ATTR_TEMPERATURE = "temperature"
ATTR_TARGET_TEMPERATURE = "target_temperature"
ATTR_INSIDE_TEMPERATURE = "inside_temperature"
ATTR_OUTSIDE_TEMPERATURE = "outside_temperature"
ATTR_WIFI_STRENGTH = "wifi_strength"
ATTR_WIFI_SSID = "wifi_ssid"
ATTR_LOCAL_SSID = "local_ssid"
ATTR_MAC_ADDRESS = "mac_address"
ATTR_SERIAL_NUMBER = "serial_number"
ATTR_ENERGY_CONSUMPTION = "energy_consumption"
ATTR_ROOM_HUMIDITY = "room_humidity"
ATTR_TARGET_HUMIDITY = "target_humidity"
ATTR_FAN_MODE = "fan_mode"
ATTR_FAN_SPEED = "fan_speed"
ATTR_HSWING_MODE = "hswing_mode"
ATTR_VSWING_MODE = "vswing_mode"
ATTR_SWING_AUTO = "auto"
ATTR_SWING_SWING = "swing"
ATTR_SWING_STOP = "stop"
ATTR_SWING_FLOOR_HEATING = "floorHeatingAirflow"
ATTR_COOL_ENERGY = "cool_energy"
ATTR_HEAT_ENERGY = "heat_energy"

MP_CLIMATE = "climateControl"
MP_GATEWAY = "gateway"
DP_ON_OFF = "onOffMode"
DP_OPERATION_MODE = "operationMode"
DP_SENSORS = "sensoryData"
DP_TEMPERATURE = "temperatureControl"
DP_FAN = "fanControl"
DP_CONSUMPTION = "consumptionData"
DP_WIFI_STRENGTH = "wifiConnectionStrength"
DP_WIFI_SSID = "wifiConnectionSSID"
DP_LOCAL_SSID = "ssid"
DP_MAC_ADDRESS = "macAddress"
DP_SERIAL_NUMBER = "serialNumber"

DAIKIN_CMD_SETS = {
    ATTR_ON_OFF: [MP_CLIMATE, DP_ON_OFF, ""],
    ATTR_PRESET_MODE: [MP_CLIMATE, "", ""],
    ATTR_OPERATION_MODE: [MP_CLIMATE, DP_OPERATION_MODE, ""],
    ATTR_OUTSIDE_TEMPERATURE: [MP_CLIMATE, DP_SENSORS, "/outdoorTemperature"],
    ATTR_INSIDE_TEMPERATURE: [MP_CLIMATE, DP_SENSORS, "/roomTemperature"],
    ATTR_ROOM_HUMIDITY: [MP_CLIMATE, DP_SENSORS, "/roomHumidity"],
    ATTR_TARGET_TEMPERATURE: [
        MP_CLIMATE,
        DP_TEMPERATURE,
        "/operationModes/%operationMode%/setpoints/roomTemperature",
    ],
    ATTR_FAN_MODE: [
        MP_CLIMATE,
        DP_FAN,
        "/operationModes/%operationMode%/fanSpeed/currentMode",
    ],
    ATTR_FAN_SPEED: [
        MP_CLIMATE,
        DP_FAN,
        "/operationModes/%operationMode%/fanSpeed/modes/fixed",
    ],
    ATTR_HSWING_MODE: [
        MP_CLIMATE,
        DP_FAN,
        "/operationModes/%operationMode%/fanDirection/horizontal/currentMode",
    ],
    ATTR_VSWING_MODE: [
        MP_CLIMATE,
        DP_FAN,
        "/operationModes/%operationMode%/fanDirection/vertical/currentMode",
    ],
    ATTR_ENERGY_CONSUMPTION: [MP_CLIMATE, DP_CONSUMPTION, "/electrical"],
    ATTR_WIFI_STRENGTH: [MP_GATEWAY, DP_WIFI_STRENGTH, ""],
    ATTR_WIFI_SSID: [MP_GATEWAY, DP_WIFI_SSID, ""],
    ATTR_LOCAL_SSID: [MP_GATEWAY, DP_LOCAL_SSID, ""],
    ATTR_MAC_ADDRESS: [MP_GATEWAY, DP_MAC_ADDRESS, ""],
    ATTR_SERIAL_NUMBER: [MP_GATEWAY, DP_SERIAL_NUMBER, ""],
}

ATTR_STATE_ON = "on"
ATTR_STATE_OFF = "off"

FAN_FIXED = "fixed"
FAN_QUIET = "Silence"

SWING_OFF = "Off"
SWING_BOTH = "3D"
SWING_VERTICAL = "Vertical"
SWING_HORIZONTAL = "Horizontal"
SWING_FLOOR_HEATING = "Floor Heating"
SWING_FLOOR_HEATING_AND_HORIZONTAL = "Floor Heating and Horizontal"

PRESET_STREAMER = "streamer"

SENSOR_TYPE_TEMPERATURE = "temperature"
SENSOR_TYPE_HUMIDITY = "humidity"
SENSOR_TYPE_GATEWAY_DIAGNOSTIC = "gateway_diagnostic"
SENSOR_TYPE_POWER = "power"
SENSOR_TYPE_ENERGY = "energy"
SENSOR_PERIOD_DAILY = "d"
SENSOR_PERIOD_WEEKLY = "w"
SENSOR_PERIOD_YEARLY = "m"
SENSOR_PERIODS = {
    SENSOR_PERIOD_DAILY: "Daily",
    SENSOR_PERIOD_WEEKLY: "Weekly",
    SENSOR_PERIOD_YEARLY: "Yearly",
}

SENSOR_TYPES = {
    ATTR_INSIDE_TEMPERATURE: {
        CONF_NAME: "Inside Temperature",
        CONF_TYPE: SENSOR_TYPE_TEMPERATURE,
        CONF_DEVICE_CLASS: DEVICE_CLASS_TEMPERATURE,
        CONF_UNIT_OF_MEASUREMENT: TEMP_CELSIUS,
    },
    ATTR_OUTSIDE_TEMPERATURE: {
        CONF_NAME: "Outside Temperature",
        CONF_TYPE: SENSOR_TYPE_TEMPERATURE,
        CONF_DEVICE_CLASS: DEVICE_CLASS_TEMPERATURE,
        CONF_UNIT_OF_MEASUREMENT: TEMP_CELSIUS,
    },
    ATTR_ROOM_HUMIDITY: {
        CONF_NAME: "Room Humidity",
        CONF_TYPE: SENSOR_TYPE_HUMIDITY,
        CONF_DEVICE_CLASS: DEVICE_CLASS_HUMIDITY,
        CONF_UNIT_OF_MEASUREMENT: PERCENTAGE,
    },
    ATTR_COOL_ENERGY: {
        CONF_NAME: "Cool Energy Consumption",
        CONF_TYPE: SENSOR_TYPE_ENERGY,
        CONF_ICON: "mdi:snowflake",
        CONF_DEVICE_CLASS: DEVICE_CLASS_ENERGY,
        CONF_UNIT_OF_MEASUREMENT: ENERGY_KILO_WATT_HOUR,
    },
    ATTR_HEAT_ENERGY: {
        CONF_NAME: "Heat Energy Consumption",
        CONF_TYPE: SENSOR_TYPE_ENERGY,
        CONF_ICON: "mdi:fire",
        CONF_DEVICE_CLASS: DEVICE_CLASS_ENERGY,
        CONF_UNIT_OF_MEASUREMENT: ENERGY_KILO_WATT_HOUR,
    },
    ATTR_WIFI_STRENGTH: {
        CONF_NAME: "WiFi Strength",
        CONF_TYPE: SENSOR_TYPE_GATEWAY_DIAGNOSTIC,
        CONF_DEVICE_CLASS: DEVICE_CLASS_SIGNAL_STRENGTH,
        CONF_UNIT_OF_MEASUREMENT: SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    },
    ATTR_WIFI_SSID: {
        CONF_NAME: "WiFi SSID",
        CONF_TYPE: SENSOR_TYPE_GATEWAY_DIAGNOSTIC,
        CONF_ICON: "mdi:access-point-network",
        CONF_DEVICE_CLASS: None,
        CONF_UNIT_OF_MEASUREMENT: None,
    },
    ATTR_LOCAL_SSID: {
        CONF_NAME: "Internal SSID",
        CONF_TYPE: SENSOR_TYPE_GATEWAY_DIAGNOSTIC,
        CONF_DEVICE_CLASS: None,
        CONF_UNIT_OF_MEASUREMENT: None,
    },
    ATTR_MAC_ADDRESS: {
        CONF_NAME: "Mac Address",
        CONF_TYPE: SENSOR_TYPE_GATEWAY_DIAGNOSTIC,
        CONF_DEVICE_CLASS: None,
        CONF_UNIT_OF_MEASUREMENT: None,
    },
    ATTR_SERIAL_NUMBER: {
        CONF_NAME: "Serial Number",
        CONF_TYPE: SENSOR_TYPE_GATEWAY_DIAGNOSTIC,
        CONF_ICON: "mdi:numeric",
        CONF_DEVICE_CLASS: None,
        CONF_UNIT_OF_MEASUREMENT: None,
    },
}

CONF_UUID = "uuid"

KEY_MAC = "mac"
KEY_IP = "ip"

TIMEOUT = 60
