"""Обработчик /start и главного меню."""
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.keyboards.main_menu import main_menu_kb
from bot.middlewares.i18n import t
from bot.handlers.storage import get_last_route, format_last_route

router = Router(name="start")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    uid = message.from_user.id
    await message.answer(
        t(uid, "welcome"),
        reply_markup=main_menu_kb(uid),
        parse_mode="HTML",
    )


@router.message(F.text.in_({"📋 Последний маршрут", "📋 Останній маршрут"}))
async def last_route_btn(message: Message) -> None:
    uid = message.from_user.id
    data = get_last_route(uid)
    if not data:
        await message.answer(t(uid, "no_last_route"))
        return
    text = f"{t(uid, 'last_route_header')}\n\n" + format_last_route(uid, data)
    await message.answer(text, parse_mode="HTML")
