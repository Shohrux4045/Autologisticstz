# Autologisticstz

## Установка

1. Клонируйте репозиторий:
    ```bash
    git clone <URL>
    ```

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

3. Настройте базу данных и выполните миграции:
    ```bash
    python manage.py migrate
    ```
5. Запустите парсер:
    ```bash
    python manage.py parse_news
    ```
5. Запустите сервер:
    ```bash
    python manage.py runserver
    ```

## Команды бота
1.Запустите бота
bot.py run main
https://t.me/Autologisticstz_bot
- `/start`: Приветственное сообщение
- `/latest`: Получить последние новости
