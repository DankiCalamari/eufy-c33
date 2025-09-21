from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

DOMAIN = "eufy_c33_lock"

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        "email": entry.data.get("email"),
        "password": entry.data.get("password"),
    }
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "lock")
    )
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    await hass.config_entries.async_forward_entry_unload(entry, "lock")
    hass.data[DOMAIN].pop(entry.entry_id)
    return True
