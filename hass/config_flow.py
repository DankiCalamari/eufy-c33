import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_EMAIL, CONF_PASSWORD
from . import DOMAIN

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_EMAIL): str,
    vol.Required(CONF_PASSWORD): str,
})

class EufyC33ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Eufy C33 Smart Lock."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step where the user enters credentials."""
        errors = {}

        if user_input is not None:
            email = user_input[CONF_EMAIL]
            password = user_input[CONF_PASSWORD]

            # TODO: Replace with real API test (pyeufy-security login)
            valid = await self._test_credentials(email, password)

            if valid:
                # Save entry to HA
                return self.async_create_entry(
                    title="Eufy C33 Lock",
                    data={
                        CONF_EMAIL: email,
                        CONF_PASSWORD: password,
                    },
                )
            else:
                errors["base"] = "auth_failed"

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )

    async def _test_credentials(self, email, password) -> bool:
        """Pretend to test credentials. Replace with real API call."""
        # TODO: Implement with pyeufy-security login check
        if email and password:
            return True
        return False
