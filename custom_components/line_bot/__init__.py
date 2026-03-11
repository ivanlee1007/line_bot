"""The line_bot component."""

import logging

from homeassistant.helpers.dispatcher import async_dispatcher_send

from linebot.models import (
    AudioSendMessage,
    ButtonsTemplate,
    ConfirmTemplate,
    FlexSendMessage,
    ImageSendMessage,
    LocationSendMessage,
    MessageAction,
    PostbackAction,
    StickerSendMessage,
    TemplateSendMessage,
    TextSendMessage,
    URIAction,
)

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN, PLATFORMS, SIGNAL_ALIAS_REGISTRY_UPDATED
from .helpers import get_quota
from .http import async_register_http
from .services import async_setup_services

_LOGGER = logging.getLogger(__name__)

MESSAGES = {
    "text": TextSendMessage,
    "image": ImageSendMessage,
    "sticker": StickerSendMessage,
    "template": TemplateSendMessage,
    "location": LocationSendMessage,
    "flex": FlexSendMessage,
    "audio": AudioSendMessage,
}


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up OpenAI Conversation."""
    await async_setup_services(hass, config)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Line Bot from a config entry."""

    await get_quota(hass, entry.data[CONF_ACCESS_TOKEN])
    hass.data.setdefault(DOMAIN, {}).setdefault("entry", {}).setdefault(
        entry.entry_id, {}
    )

    async def _async_handle_entry_update(hass: HomeAssistant, updated_entry: ConfigEntry):
        """Handle config entry updates."""
        async_dispatcher_send(
            hass,
            f"{SIGNAL_ALIAS_REGISTRY_UPDATED}_{updated_entry.entry_id}",
        )

    entry.async_on_unload(entry.add_update_listener(_async_handle_entry_update))

    async_register_http(hass)
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    async_dispatcher_send(hass, f"{SIGNAL_ALIAS_REGISTRY_UPDATED}_{entry.entry_id}")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload Line Bot."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN]["entry"].pop(entry.entry_id)
    return unload_ok
