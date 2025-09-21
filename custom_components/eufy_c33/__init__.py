import asyncio
import logging
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, PLATFORMS, DEFAULT_TIMEOUT
from .eufy_api import EufyC33API

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(seconds=30)

class EufyC33DataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, api: EufyC33API) -> None:
        self.api = api
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=SCAN_INTERVAL,
        )

    async def _async_update_data(self):
        try:
            return await self.api.get_status()
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    
    api = EufyC33API(
        host=entry.data["host"],
        mac_address=entry.data.get("mac_address"),
        local_key=entry.data.get("local_key"),
        timeout=DEFAULT_TIMEOUT
    )
    
    coordinator = EufyC33DataUpdateCoordinator(hass, api)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }
    
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok