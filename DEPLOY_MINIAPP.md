Короткая инструкция как развернуть мини‑приложение и убрать 404 в Telegram WebApp

1) Кому положить файлы на GitHub

- Рекомендуемый вариант: создать отдельный публичный репозиторий (например `TG_LOGISTPRO`) и в корень положить файлы из папки `miniapp/` (в корне должны быть `index.html`, `manifest.json`, `404.html` и др.).

2) Быстро через Git (если у вас пустой/новый репозиторий):

```bash
# перейдите в папку miniapp или в директорию с файлами
cd "d:/Project AI/TGBOT_LOGISTIKA/miniapp"
# инициализировать локальный репозиторий и запушить в GitHub
git init
git add .
git commit -m "Deploy miniapp"
git branch -M main
git remote add origin https://github.com/mynameneon/TG_LOGISTPRO.git
git push -u origin main
```

3) Если репозиторий уже есть и вы редактируете через веб‑интерфейс

- Зайдите в https://github.com/mynameneon/TG_LOGISTPRO и нажмите `Add file → Upload files` и загрузите содержимое `miniapp/` (включая `404.html`). Commit.

4) Включите GitHub Pages

- Откройте Settings → Pages (или Pages & deployments) в репозитории → выберите Branch = `main` и Folder = `/ (root)` → Save.
- Подождите ~1–5 минут.

5) Обновите `.env` в проекте бота (локально, НЕ пушьте `.env` в публичный репозиторий!)

Откройте `d:/Project AI/TGBOT_LOGISTIKA/.env` и установите:

```
MINIAPP_URL=https://mynameneon.github.io/TG_LOGISTPRO/index.html
```

6) Перезапустите бота (локально) и проверьте логи — бот теперь логирует `MINIAPP_URL` при старте.

Windows (PowerShell):
```powershell
cd "d:/Project AI/TGBOT_LOGISTIKA"
python -m bot.main
```

7) Тестирование

- Откройте `https://mynameneon.github.io/TG_LOGISTPRO/` в мобильном браузере (на том же устройстве, где запускаете Telegram) — должно открываться.
- Затем в Telegram нажмите кнопку навигатора — должно открыться веб‑приложение без 404.

8) Если всё ещё 404

- Попробуйте временно в `.env` указать `MINIAPP_URL` с явным `index.html` (см. шаг 5). Я уже сделал это локально.
- Убедитесь, что репозиторий публичный и `404.html` присутствует в корне Pages (это позволяет корректно перенаправлять запросы, которые Telegram может формировать с путями).

9) Важно

- Никогда не пушьте `BOT_TOKEN` или `.env` в публичный репозиторий. Если токен уже утёк — регенерируйте его в BotFather.

Если хочешь, я могу подготовить коммит (готово локально) — тебе останется только выполнить `git add/commit/push` в репо, куда нужно развернуть (или залить через GitHub UI). Напиши, хочешь ли пошагово команды для твоего случая.
