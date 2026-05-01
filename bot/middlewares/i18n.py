"""Простая i18n: язык пользователя + переводы из JSON."""
import json
from pathlib import Path

LOCALES_DIR = Path(__file__).resolve().parent.parent / "locales"

# Загружаем переводы один раз при старте
_translations: dict[str, dict[str, str]] = {}
for locale_file in LOCALES_DIR.glob("*.json"):
    lang = locale_file.stem
    with open(locale_file, "r", encoding="utf-8") as f:
        _translations[lang] = json.load(f)

# Язык пользователей в памяти: user_id -> "ru" | "ua"
_user_langs: dict[int, str] = {}

DEFAULT_LANG = "ru"
SUPPORTED_LANGS = ("ru", "ua")


def get_user_lang(user_id: int) -> str:
    return _user_langs.get(user_id, DEFAULT_LANG)


def set_user_lang(user_id: int, lang: str) -> None:
    if lang in SUPPORTED_LANGS:
        _user_langs[user_id] = lang


def t(user_id: int, key: str, **kwargs) -> str:
    lang = get_user_lang(user_id)
    text = _translations.get(lang, {}).get(key) or _translations[DEFAULT_LANG].get(key, key)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text
