import asyncio
from datetime import datetime, timezone
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import ClientSession

API_TOKEN = '6806297053:AAHLGv0mBk_EyNtWJdTax7MuCEkCK7wJioc'  # Замените на ваш токен

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

API_URL = 'http://localhost:8000/api/news/'  # Замените на URL вашего API

async def get_latest_news():
    async with ClientSession() as session:
        async with session.get(API_URL) as response:
            if response.status == 200:
                news = await response.json()
                return news[:10]  # Возвращаем последние 10 новостей
            return []

@dp.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.answer("Привет! Используйте команду /latest, чтобы получить последние новости.")

@dp.message(Command('latest'))
async def send_latest_news(message: types.Message):
    news_items = await get_latest_news()
    if news_items:
        for item in news_items:
            # Замените <br> на \n и убедитесь, что используете только поддерживаемые теги
            text = f"<b>{item['title']}</b>\n{item['text']}\n{item['link']}"
            await message.answer(text, parse_mode='HTML')
    else:
        await message.answer("Нет доступных новостей.")

async def notify_new_news():
    last_checked = datetime.now(timezone.utc)
    while True:
        await asyncio.sleep(3600)  # Проверяем каждые 60 минут
        news_items = await get_latest_news()
        for item in news_items:
            if datetime.fromisoformat(item['publication_date']).astimezone(timezone.utc) > last_checked:
                text = f"Новая новость: <b>{item['title']}</b>\n{item['text']}\n{item['link']}"
                await bot.send_message(chat_id='YOUR_CHAT_ID', text=text, parse_mode='HTML')
        last_checked = datetime.now(timezone.utc)

async def main():
    asyncio.create_task(notify_new_news())
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
