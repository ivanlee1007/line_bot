"""Helper functions for Line Bot integration."""

from datetime import datetime
from functools import partial

from linebot import LineBotApi

from homeassistant.core import HomeAssistant
import homeassistant.util.dt as dt_util

from .const import CONF_ALLOWED_CHAT_IDS, CONF_CHAT_ID, DOMAIN


async def get_quota(hass: HomeAssistant, access_token: str):
    """Get quota for the Line Bot API."""
    line_bot = LineBotApi(access_token)

    await hass.loop.run_in_executor(
        None, partial(line_bot.get_message_quota_consumption)
    )


def get_config_entry(hass: HomeAssistant):
    """Get the config entry."""
    entry_data = hass.data.get(DOMAIN, {}).get("entry", {})
    entry_id, data = next(iter(entry_data.items()), (None, None))
    return hass.config_entries.async_get_entry(entry_id)


def get_data(hass: HomeAssistant):
    """Get the data."""
    entry_id, data = next(iter(hass.data[DOMAIN]["entry"].items()))
    return data


def get_allowed_chat_ids(hass: HomeAssistant) -> dict:
    """Get the configured allowed chat ids."""
    entry = get_config_entry(hass)
    if entry is None:
        return {}
    return entry.data.get(CONF_ALLOWED_CHAT_IDS, {})


def get_public_alias_registry(hass: HomeAssistant) -> dict:
    """Get public alias registry data for UI/entity exposure."""
    allowed_chat_ids = get_allowed_chat_ids(hass)
    aliases = sorted(allowed_chat_ids)
    updated_at: datetime = dt_util.now()
    return {
        "count": len(aliases),
        "aliases": aliases,
        "updated_at": updated_at.isoformat(),
    }


def get_detailed_alias_registry(hass: HomeAssistant, include_chat_id: bool = True) -> dict:
    """Get detailed alias registry data for service responses/debugging."""
    allowed_chat_ids = get_allowed_chat_ids(hass)
    chats = []

    for alias in sorted(allowed_chat_ids):
        chat = {"alias": alias}
        chat_id = allowed_chat_ids.get(alias, {}).get(CONF_CHAT_ID)
        if include_chat_id:
            chat[CONF_CHAT_ID] = chat_id
        chats.append(chat)

    response = {
        "count": len(chats),
        "aliases": [chat["alias"] for chat in chats],
        "chats": chats,
        "updated_at": dt_util.now().isoformat(),
    }
    if include_chat_id:
        response["mapping"] = {
            chat["alias"]: chat.get(CONF_CHAT_ID) for chat in chats
        }
    return response
