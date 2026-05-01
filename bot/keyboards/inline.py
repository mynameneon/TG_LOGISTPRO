"""Инлайн-клавиатуры."""
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    WebAppInfo,
)

from bot.config import MINIAPP_URL
from bot.middlewares.i18n import t


def language_kb() -> InlineKeyboardMarkup:
    """Выбор языка."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang:ru"),
                InlineKeyboardButton(text="🇺🇦 Українська", callback_data="lang:ua"),
            ]
        ]
    )


def open_navigator_kb(user_id: int) -> InlineKeyboardMarkup:
    """Инлайн-кнопка открытия Mini App."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=t(user_id, "open_again"),
                    web_app=WebAppInfo(url=MINIAPP_URL),
                )
            ]
        ]
    )
