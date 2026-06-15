# TodoBot

**TodoBot** — это простой Telegram-бот для создания и управления списком дел. Бот позволяет добавлять, просматривать и удалять задачи, а также отмечать их как выполненные.

## Возможности

  Добавление новых задач
  Просмотр текущего списка дел
  Отметка задач как выполненных
  Удаление задач
  Хранение задач в базе данных (SQLite)

## Установка и запуск

Для запуска бота потребуется Python 3.9 или новее и токен бота от [@BotFather](https://t.me/BotFather).

### Клонирование репозитория

```bash
git clone https://github.com/ScorpiOVN-SC/TodoBot.git
cd TodoBot
```

### Создание виртуального окружения

```bash
python -m venv venv
venv\Scripts\activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Настройка токена

В файле config.py необходимо заменить TOKEN на токен, который вы получили в BotFather

```bash
TOKEN = "token"
```

## Зависимости

```bash
pyTelegramBotAPI == 4.33.0
```
