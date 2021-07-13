"""Platform for the Daikin AC."""
import asyncio
import datetime
import logging
import requests
import json
import time
import voluptuous as vol

from homeassistant.config_entries import SOURCE_IMPORT, ConfigEntry

# from homeassistant.exceptions import ConfigEntryNotReady
# import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import HomeAssistantType
from homeassistant.util import Throttle

from .const import DOMAIN, DAIKIN_API, DAIKIN_DEVICES

from .daikin_base import Appliance

_LOGGER = logging.getLogger(__name__)

ENTRY_IS_SETUP = "daikin_entry_is_setup"

PARALLEL_UPDATES = 0

SERVICE_FORCE_UPDATE = "force_update"
SERVICE_PULL_DEVICES = "pull_devices"

SIGNAL_DELETE_ENTITY = "daikin_delete"
SIGNAL_UPDATE_ENTITY = "daikin_update"

TOKENSET_FILE = "tokenset.json"

MIN_TIME_BETWEEN_UPDATES = datetime.timedelta(seconds=15)
REQUEST_DELAY_TIME_s = 5

COMPONENT_TYPES = ["climate", "sensor", "switch"]
# COMPONENT_TYPES = ["sensor", "switch"]


CONFIG_SCHEMA = vol.Schema(vol.All({DOMAIN: vol.Schema({})}), extra=vol.ALLOW_EXTRA)


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

    daikin_api = DaikinApi(hass)
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


class DaikinApi:
    """Daikin Residential API."""

    def __init__(self, hass):
        """Initialize a new Daikin Residential API."""
        #        super()
        self.hass = hass
        self.tokenSet = None
        self._delay_next_request = False
        tokenFile = self.hass.config.path(TOKENSET_FILE)
        _LOGGER.info("Initialing Daikin Residential API (%s)...", tokenFile)
        try:
            with open(tokenFile) as jsonFile:
                jsonObject = json.load(jsonFile)
                self.tokenSet = jsonObject
                jsonFile.close()
        except IOError:
            _LOGGER.error("tokenset.json file not found in config folder.")
            raise Exception("tokenset.json file not found in config folder.")

        _LOGGER.info("Initialized Daikin Residential API")
        _LOGGER.debug(
            "Daikin Residential API token is [%s]", self.tokenSet["access_token"]
        )

    async def doBearerRequest(self, resourceUrl, options=None, refreshed=False):
        if self.tokenSet is None:
            raise Exception(
                "Please provide a TokenSet or use the Proxy server to Authenticate once"
            )

        if not resourceUrl.startswith("http"):
            resourceUrl = "https://api.prod.unicloud.edc.dknadmin.be" + resourceUrl

        headers = {
            "user-agent": "Daikin/1.6.1.4681 CFNetwork/1209 Darwin/20.2.0",
            "x-api-key": "xw6gvOtBHq5b1pyceadRp6rujSNSZdjx2AqT03iC",
            "Authorization": "Bearer " + self.tokenSet["access_token"],
            "Content-Type": "application/json",
        }

        _LOGGER.debug("BEARER REQUEST URL: %s", resourceUrl)
        _LOGGER.debug("BEARER REQUEST HEADERS: %s", headers)
        if options is not None and "method" in options and options["method"] == "PATCH":
            _LOGGER.debug("BEARER REQUEST JSON: %s", options["json"])
            res = requests.patch(resourceUrl, headers=headers, data=options["json"])
        else:
            try:
                func = functools.partial(
                    requests.get,
                    resourceUrl,
                    headers=headers,
                )
                res = await self.hass.async_add_executor_job(requests.get,resourceUrl,headers)
                #res = requests.get(resourceUrl, headers=headers)
            except Exception as e:
                _LOGGER.error("REQUEST FAILED: %s", e)
        _LOGGER.debug("BEARER RESPONSE CODE: %s", res.status_code)

        if res.status_code == 200:
            try:
                return res.json()
            except Exception:
                return res.text
        if res.status_code == 204:
            return True

        if not refreshed and res.status_code == 401:
            _LOGGER.info("TOKEN EXPIRED: will refresh it (%s)", res.status_code)
            await self.refreshAccessToken()
            return await self.doBearerRequest(resourceUrl, options, True)

        raise Exception("Communication failed! Status: " + str(res.status_code))

    async def refreshAccessToken(self):
        """Attempt to refresh the Access Token."""
        url = "https://cognito-idp.eu-west-1.amazonaws.com"

        headers = {
            "Content-Type": "application/x-amz-json-1.1",
            "x-amz-target": "AWSCognitoIdentityProviderService.InitiateAuth",
            "x-amz-user-agent": "aws-amplify/0.1.x react-native",
            "User-Agent": "Daikin/1.6.1.4681 CFNetwork/1220.1 Darwin/20.3.0",
        }
        ref_json = {
            "ClientId": "7rk39602f0ds8lk0h076vvijnb",
            "AuthFlow": "REFRESH_TOKEN_AUTH",
            "AuthParameters": {"REFRESH_TOKEN": self.tokenSet["refresh_token"]},
        }
        res = requests.post(url, headers=headers, json=ref_json)
        _LOGGER.info("REFRESHACCESSTOKEN RESPONSE CODE: %s", res.status_code)
        _LOGGER.debug("REFRESHACCESSTOKEN RESPONSE: %s", res.json())
        res_json = res.json()

        if (
            res_json["AuthenticationResult"] is not None
            and res_json["AuthenticationResult"]["AccessToken"] is not None
            and res_json["AuthenticationResult"]["TokenType"] == "Bearer"
        ):
            self.tokenSet["access_token"] = res_json["AuthenticationResult"][
                "AccessToken"
            ]
            self.tokenSet["id_token"] = res_json["AuthenticationResult"]["IdToken"]
            self.tokenSet["expires_at"] = int(
                datetime.datetime.now().timestamp()
            ) + int(res_json["AuthenticationResult"]["ExpiresIn"])
            _LOGGER.debug("NEW TOKENSET: %s", self.tokenSet)
            tokenFile = self.hass.config.path(TOKENSET_FILE)
            with open(tokenFile, "w") as outfile:
                json.dump(self.tokenSet, outfile)

            #            self.emit('token_update', self.tokenSet);
            return self.tokenSet
        raise Exception(
            "Token refresh was not successful! Status: " + str(res.status_code)
        )

    async def getApiInfo(self):
        """Get Daikin API Info."""
        return await self.doBearerRequest("/v1/info")

    async def getCloudDeviceDetails(self):
        """Get pure Device Data from the Daikin cloud devices."""
        return await self.doBearerRequest("/v1/gateway-devices")

    async def getCloudDevices(self):
        """Get array of DaikinResidentialDevice objects and get their data."""
        devices = await self.getCloudDeviceDetails()
        res = {}
        for dev in devices or []:
            res[dev["id"]] = Appliance(dev, self)
        return res

    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    async def async_update(self, **kwargs):
        """Pull the latest data from Daikin."""
        _LOGGER.debug("API UPDATE")
        if self._delay_next_request:
            _LOGGER.debug("SLEEPING FOR %i secs.", REQUEST_DELAY_TIME_s)
            time.sleep(REQUEST_DELAY_TIME_s)
            self._delay_next_request = False

        json_data = await self.getCloudDeviceDetails()
        for dev_data in json_data or []:
            self.hass.data[DOMAIN][DAIKIN_DEVICES][dev_data["id"]].setJsonData(dev_data)
