"""Конфигурация бота: токен и URL Mini App."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из корня проекта
ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
MINIAPP_URL = os.getenv(
    "MINIAPP_URL",
    "https://your-username.github.io/logistics-miniapp/",
).strip()

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не задан. Проверьте файл .env")
