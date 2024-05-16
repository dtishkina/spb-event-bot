import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession
from config import API_TOKEN
from handlers.common import register_common_handlers
from handlers.new_holland import register_new_holland_handlers
from handlers.sevcable_port import register_sevcable_port_handlers

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Инициализация сессии и бота
session = AiohttpSession()
bot = Bot(token=API_TOKEN, session=session)

# Создание диспетчера
dp = Dispatcher()

# Регистрация обработчиков
register_common_handlers(dp)
register_new_holland_handlers(dp)
register_sevcable_port_handlers(dp)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
