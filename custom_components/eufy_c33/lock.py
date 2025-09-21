import logging
from typing import Any

from homeassistant.components.lock import LockEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, ATTR_BATTERY_LEVEL, ATTR_WIFI_SIGNAL, LOCK_STATES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]
    
    async_add_entities([EufyC33Lock(coordinator, api, config_entry)])

class EufyC33Lock(CoordinatorEntity, LockEntity):
    def __init__(self, coordinator, api, config_entry):
        super().__init__(coordinator)
        self._api = api
        self._config_entry = config_entry
        self._attr_name = f"Eufy C33 Lock"
        self._attr_unique_id = f"eufy_c33_{config_entry.entry_id}"

    @property
    def is_locked(self) -> bool | None:
        """Return true if the lock is locked."""
        if self.coordinator.data:
            return self.coordinator.data.get("locked", False)
        return None

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self.coordinator.last_update_success

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        attrs = {}
        if self.coordinator.data:
            data = self.coordinator.data
            if "battery_level" in data:
                attrs[ATTR_BATTERY_LEVEL] = data["battery_level"]
            if "wifi_signal" in data:
                attrs[ATTR_WIFI_SIGNAL] = data["wifi_signal"]
            if "lock_state" in data:
                state_code = data["lock_state"]
                attrs["lock_state_description"] = LOCK_STATES.get(state_code, "unknown")
            if "last_action" in data:
                attrs["last_action"] = data["last_action"]
        return attrs

    async def async_lock(self, **kwargs: Any) -> None:
        """Lock the door."""
        success = await self._api.lock()
        if success:
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to lock the door")

    async def async_unlock(self, **kwargs: Any) -> None:
        """Unlock the door."""
        success = await self._api.unlock()
        if success:
            await self.coordinator.async_request_refresh()
        else:
            _LOGGER.error("Failed to unlock the door")

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._config_entry.entry_id)},
            "name": "Eufy C33 Door Lock",
            "manufacturer": "Eufy",
            "model": "C33",
            "sw_version": "1.0.0",
        }