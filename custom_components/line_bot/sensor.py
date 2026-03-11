"""Sensor platform for Line Bot alias registry."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.dispatcher import async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, SIGNAL_ALIAS_REGISTRY_UPDATED
from .helpers import get_public_alias_registry


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Line Bot sensors from a config entry."""
    async_add_entities([LineBotAliasRegistrySensor(hass, entry)], True)


class LineBotAliasRegistrySensor(SensorEntity):
    """Expose the public Line Bot alias registry."""

    _attr_has_entity_name = True
    _attr_icon = "mdi:account-box-multiple"

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        self.hass = hass
        self.entry = entry
        self._attr_unique_id = f"{entry.entry_id}_alias_registry"
        self._attr_name = "Alias Registry"
        self._attr_native_value = 0
        self._attr_extra_state_attributes = {
            "aliases": [],
            "updated_at": None,
        }
        self._refresh_state()

    @property
    def device_info(self):
        """Return device information for this entity."""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": "Line Bot",
            "manufacturer": "LINE",
            "model": "Messaging API",
        }

    async def async_added_to_hass(self) -> None:
        """Handle entity which will be added."""
        self.async_on_remove(
            async_dispatcher_connect(
                self.hass,
                f"{SIGNAL_ALIAS_REGISTRY_UPDATED}_{self.entry.entry_id}",
                self._handle_registry_update,
            )
        )

    def _refresh_state(self) -> None:
        """Refresh sensor state from the current config entry data."""
        registry = get_public_alias_registry(self.hass)
        self._attr_native_value = registry["count"]
        self._attr_extra_state_attributes = {
            "aliases": registry["aliases"],
            "updated_at": registry["updated_at"],
        }

    def _handle_registry_update(self) -> None:
        """Handle alias registry update signal."""
        self._refresh_state()
        self.async_write_ha_state()
