"""Platform for the Daikin AC."""
import asyncio
import datetime
import logging
import voluptuous as vol

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from homeassistant.helpers.typing import HomeAssistantType

from .const import DOMAIN, DAIKIN_API, DAIKIN_DEVICES

from .daikin_api import DaikinApi

_LOGGER = logging.getLogger(__name__)

ENTRY_IS_SETUP = "daikin_entry_is_setup"

PARALLEL_UPDATES = 0

SERVICE_FORCE_UPDATE = "force_update"
SERVICE_PULL_DEVICES = "pull_devices"

SIGNAL_DELETE_ENTITY = "daikin_delete"
SIGNAL_UPDATE_ENTITY = "daikin_update"

TOKENSET_FILE = "tokenset.json"

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(seconds=15)

COMPONENT_TYPES = ["climate", "sensor", "switch"]


CONFIG_SCHEMA = vol.Schema(
    vol.All(
        {
            DOMAIN: vol.Schema(
                {vol.Required(CONF_EMAIL): str, vol.Required(CONF_PASSWORD): str}
            )
        }
    ),
    extra=vol.ALLOW_EXTRA,
)


async def async_setup(hass, config):
    """Establish connection with Daikin."""
    if DOMAIN not in config:
        return True

    conf = config.get(DOMAIN)
    if conf is not None:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": SOURCE_IMPORT}, data=conf
            )
        )
    return True


async def async_setup_entry(hass: HomeAssistantType, entry: ConfigEntry):
    """Establish connection with Daikin."""

    daikin_api = DaikinApi(hass, entry)
    await daikin_api.getCloudDeviceDetails()

    devices = await daikin_api.getCloudDevices()
    hass.data[DOMAIN] = {DAIKIN_API: daikin_api, DAIKIN_DEVICES: devices}

    for component in COMPONENT_TYPES:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, component)
        )
    return True


async def async_unload_entry(hass, config_entry):
    """Unload a config entry."""
    await asyncio.wait(
        [
            hass.config_entries.async_forward_entry_unload(config_entry, component)
            for component in COMPONENT_TYPES
        ]
    )
    hass.data[DOMAIN].pop(config_entry.entry_id)
    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)
    return True


async def daikin_api_setup(hass, host, key, uuid, password):
    """Create a Daikin instance only once."""
    return
