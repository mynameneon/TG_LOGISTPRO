"""Главное меню бота с Web App кнопкой."""
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
)

from bot.config import MINIAPP_URL
from bot.middlewares.i18n import t


def main_menu_kb(user_id: int) -> ReplyKeyboardMarkup:
    """Главная клавиатура с Web App кнопкой навигатора."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=t(user_id, "open_navigator"),
                    web_app=WebAppInfo(url=MINIAPP_URL),
                )
            ],
            [
                KeyboardButton(text=t(user_id, "last_route")),
                KeyboardButton(text=t(user_id, "settings")),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="🚗",
    )
