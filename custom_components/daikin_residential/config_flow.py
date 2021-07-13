"""Config flow for the Daikin platform."""
import logging

import voluptuous as vol

from homeassistant import config_entries

from .daikin_api import DaikinApi
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


@config_entries.HANDLERS.register(DOMAIN)
class FlowHandler(config_entries.ConfigFlow):
    """Handle a config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize the Daikin config flow."""
        self.host = None

    @property
    def schema(self):
        """Return current schema."""
        return vol.Schema({})

    async def _create_entry(self):
        """Register new entry."""
        # if not self.unique_id:
        #    await self.async_set_unique_id(password)
        # self._abort_if_unique_id_configured()
        if self._async_current_entries():
            return self.async_abort(reason="already_configured")

        await self.async_set_unique_id("DaikinResidentialController")

        return self.async_create_entry(title="Daikin", data={})

    async def _attempt_connection(self):
        """Create device."""
        try:
            daikin_api = DaikinApi(self.hass)
        except Exception:
            return self.async_abort(reason="missing_config")
        try:
            await daikin_api.getApiInfo()
        except Exception:
            return self.async_abort(reason="cannot_connect")

        return await self._create_entry()

    async def async_step_user(self, user_input=None):
        """User initiated config flow."""
        if user_input is None:
            return self.async_show_form(step_id="user", data_schema=self.schema)
        return await self._attempt_connection()

    async def async_step_import(self, user_input):
        """Import a config entry."""
        return await self._create_entry()
