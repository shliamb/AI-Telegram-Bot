# AI Telegram Bot

[🇷🇺 Русский](#русский) | [🇬🇧 English](#english)

---

## Русский

Проект написан около двух лет назад и на сегодняшний день сильно устарел. Выкладываю как есть, за неактуальностью — возможно, кому-то пригодится.

**Что делает:**

Telegram-бот с доступом к разным AI-моделям. Принимает текст, изображения, документы и голосовые сообщения. Поддерживает файлы: `docx`, `pdf`, `json`, `txt`, `md`, `xlsx`, `csv`, `jpg`, `png`.

Умеет:
- хранить историю диалога в PostgreSQL;
- переключаться между моделями прямо в разговоре, сохраняя контекст;
- выкачивать список клиентов в JSON;
- транскрибировать голосовые сообщения через Whisper;
- озвучивать ответы через TTS.

Вся работа с моделями идёт через сторонний API-проект со своими правилами.

**Запуск:**

```bash
cp .env_exemple .env
# заполнить .env своими ключами
docker-compose up -d --build
```

Таблицы в БД создаются вручную — командой `/crTabDb` в админ-чате.

---

## English

This project was written about two years ago and is heavily outdated today. Publishing it as-is, since it's no longer maintained — maybe someone will find it useful.

**What it does:**

A Telegram bot with access to various AI models. Accepts text, images, documents, and voice messages. Supported files: `docx`, `pdf`, `json`, `txt`, `md`, `xlsx`, `csv`, `jpg`, `png`.

Features:
- stores dialog history in PostgreSQL;
- switches between models on the fly while keeping conversation context;
- exports the client list to JSON;
- transcribes voice messages via Whisper;
- voices answers via TTS.

All model calls go through a third-party API project with its own rules.

**Run:**

```bash
cp .env_exemple .env
# fill .env with your keys
docker-compose up -d --build
```

DB tables are created manually — via the `/crTabDb` command in the admin chat.