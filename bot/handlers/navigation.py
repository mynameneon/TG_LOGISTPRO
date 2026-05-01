"""Обработка данных от Mini App через web_app_data."""
import json
import logging

from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards.inline import open_navigator_kb
from bot.middlewares.i18n import t
from bot.handlers.storage import (
    save_last_route,
    format_route,
    format_completion,
)

router = Router(name="navigation")
log = logging.getLogger(__name__)


@router.message(F.web_app_data)
async def handle_webapp_data(message: Message) -> None:
    uid = message.from_user.id
    raw = message.web_app_data.data
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        log.warning("Некорректный JSON от Mini App: %s", raw)
        await message.answer("❌ Некорректные данные от Mini App.")
        return

    action = data.get("action")

    if action == "start_route":
        save_last_route(uid, data)
        await message.answer(
            format_route(uid, data),
            parse_mode="HTML",
            reply_markup=open_navigator_kb(uid),
        )
    elif action == "route_complete":
        await message.answer(
            format_completion(uid, data),
            parse_mode="HTML",
            reply_markup=open_navigator_kb(uid),
        )
    elif action == "set_language":
        # Mini App сообщил о смене языка (RU/UA)
        from bot.middlewares.i18n import set_user_lang
        lang = data.get("lang", "ru")
        set_user_lang(uid, lang)
        await message.answer(t(uid, "language_changed"))
    else:
        await message.answer(t(uid, "unknown_action"))
