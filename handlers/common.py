from aiogram import Dispatcher, types
from aiogram.filters.command import Command
from services.keyboards import get_inline_keyboard

async def send_welcome(message: types.Message):
    await message.answer(
        "Нажмите на одну из кнопок ниже, чтобы получить информацию о мероприятиях:",
        reply_markup=get_inline_keyboard()
    )

def register_common_handlers(dp: Dispatcher):
    dp.message.register(send_welcome, Command(commands=['start']))
