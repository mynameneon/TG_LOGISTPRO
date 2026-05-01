# 🚗📦 Логист — Telegram Bot + Mini App

Telegram-бот и встроенное мини-приложение (Web App) — навигатор-логист для курьеров
и водителей в Киеве. Позволяет добавлять точки доставки, автоматически строит
оптимальный маршрут (задача коммивояжёра через OSRM Trip API) и ведёт водителя
по нему в режиме heading-up навигации.

## 🧩 Стек

- **Backend**: Python 3.11+, [aiogram 3.x](https://docs.aiogram.dev/)
- **Mini App**: одиночный `index.html` (Vanilla JS + Leaflet.js)
- **Карты**: CartoDB Dark Matter (OSM тайлы)
- **Маршруты**: публичный OSRM (`router.project-osrm.org`)
- **Геокодинг**: Nominatim (только Украина/Киев)

## 📁 Структура

```
TGBOT_LOGISTIKA/
├── bot/
│   ├── main.py              # запуск polling
│   ├── config.py            # BOT_TOKEN, MINIAPP_URL из .env
│   ├── handlers/            # /start, web_app_data, settings
│   ├── keyboards/           # ReplyKeyboard + Inline
│   ├── middlewares/i18n.py  # простая i18n RU/UA
│   ├── locales/             # ru.json, ua.json
│   └── utils/               # route_optimizer.py (fallback)
├── miniapp/
│   ├── index.html           # ВЕСЬ фронтенд (один файл)
│   └── manifest.json
├── requirements.txt
├── .env                     # BOT_TOKEN + MINIAPP_URL
├── Dockerfile
└── README.md
```

## 🚀 Быстрый старт

### 1. Установка бота

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

Отредактируйте `.env`:
```
BOT_TOKEN=ваш_токен_от_BotFather
MINIAPP_URL=https://your-username.github.io/logistics-miniapp/
```

### 2. Деплой Mini App (GitHub Pages)

1. Создайте новый публичный репозиторий (например, `logistics-miniapp`).
2. Залейте **только** содержимое папки `miniapp/` в корень репозитория.
3. В настройках: **Settings → Pages → Source: Deploy from a branch → main → /(root)**.
4. Через пару минут получите URL `https://<username>.github.io/logistics-miniapp/`.
5. Вставьте этот URL в `.env` как `MINIAPP_URL`.

> ⚠️ Mini App **обязательно** должен быть на HTTPS — иначе геолокация и сенсоры не работают.

### 3. Привязка Mini App к боту (опционально)

В [@BotFather](https://t.me/BotFather):
```
/mybots → <ваш бот> → Bot Settings → Menu Button → Edit menu button URL
```
Вставьте `MINIAPP_URL`. Теперь внизу чата появится постоянная кнопка навигатора.

### 4. Запуск бота

```bash
python -m bot.main
```

## 🐳 Docker

```bash
docker build -t logistika-bot .
docker run --rm --env-file .env logistika-bot
```

## ✨ Что внутри Mini App

- **Экран 1**: список точек с редактированием/удалением, подсказки адресов через Nominatim.
- **Экран 2**: карта с пронумерованными маркерами, линия маршрута, карточка со статистикой.
- **Экран 3**: полноэкранный heading-up навигатор — карта поворачивается по курсу,
  маркер пользователя с пульсацией, HUD с текущей точкой, кнопки «Доставлено / Пропустить».
- **Экран 4**: отчёт — выполнено/пройдено/время и кнопка «Отправить отчёт в бот».

Работают Telegram `MainButton`, `BackButton`, `HapticFeedback`, тёмная тема, RU/UA переключение
без перезагрузки.

## 📨 Обмен данными

Mini App → Bot (через `Telegram.WebApp.sendData`):

```json
{ "action":"start_route", "stops":[...], "total_distance":"12.4 км", "total_time":"~35 мин" }
{ "action":"route_complete", "done":3, "total":3, "total_distance":"14.2 км", "total_time":"42 мин" }
{ "action":"set_language", "lang":"ua" }
```

Бот форматирует и присылает удобные сообщения на языке пользователя.

## ⚠️ Примечания

- Nominatim лимит: 1 req/sec — в коде используется debounce 500 мс.
- OSRM публичный сервер бывает медленным. Есть fallback: nearest-neighbor на JS.
- Поворот карты требует компаса устройства или движения (для вычисления bearing).
  На десктопе используется обычный north-up.
- На iOS для `DeviceOrientationEvent` нужно разрешение — запрашивается автоматически.
