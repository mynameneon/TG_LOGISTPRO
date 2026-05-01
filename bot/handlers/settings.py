"""Настройки: выбор языка RU/UA."""
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from bot.keyboards.inline import language_kb
from bot.keyboards.main_menu import main_menu_kb
from bot.middlewares.i18n import t, set_user_lang

router = Router(name="settings")


@router.message(Command("settings"))
@router.message(F.text.in_({"⚙️ Настройки", "⚙️ Налаштування"}))
async def cmd_settings(message: Message) -> None:
    uid = message.from_user.id
    await message.answer(t(uid, "choose_language"), reply_markup=language_kb())


@router.callback_query(F.data.startswith("lang:"))
async def set_lang_cb(cb: CallbackQuery) -> None:
    uid = cb.from_user.id
    lang = cb.data.split(":", 1)[1]
    set_user_lang(uid, lang)
    await cb.message.edit_text(t(uid, "language_changed"))
    await cb.message.answer(
        t(uid, "welcome"),
        reply_markup=main_menu_kb(uid),
        parse_mode="HTML",
    )
    await cb.answer()
