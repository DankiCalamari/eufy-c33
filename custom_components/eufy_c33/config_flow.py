import logging
import voluptuous as vol
from typing import Any

from homeassistant import config_entries
from homeassistant.const import CONF_HOST
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN, CONF_MAC_ADDRESS, CONF_LOCAL_KEY
from .eufy_api import EufyC33API

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST): str,
        vol.Optional(CONF_MAC_ADDRESS): str,
        vol.Optional(CONF_LOCAL_KEY): str,
    }
)

class EufyC33ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )

        errors = {}

        try:
            info = await validate_input(self.hass, user_input)
        except CannotConnect:
            errors["base"] = "cannot_connect"
        except InvalidAuth:
            errors["base"] = "invalid_auth"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )

async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    api = EufyC33API(
        host=data[CONF_HOST],
        mac_address=data.get(CONF_MAC_ADDRESS),
        local_key=data.get(CONF_LOCAL_KEY)
    )
    
    try:
        status = await api.get_status()
        if not status:
            raise CannotConnect
    except Exception:
        raise CannotConnect
    
    return {"title": f"Eufy C33 Lock ({data[CONF_HOST]})"}

class CannotConnect(HomeAssistantError):
    pass

class InvalidAuth(HomeAssistantError):
    pass