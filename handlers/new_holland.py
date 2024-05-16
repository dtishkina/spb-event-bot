from aiogram import Dispatcher, types
from services.fetch_events import fetch_new_holland_events

async def handle_new_holland(callback_query: types.CallbackQuery):
    await callback_query.answer("Загружаем мероприятия Новой Голландии...")
    events_info = await fetch_new_holland_events()

    await callback_query.message.delete()

    if events_info:
        for event in events_info:
            text_message = f"{event['date']} - {event['name']}\n<a href='{event['event_url']}'>Подробнее...</a>"
            if event.get('img_url'):
                await callback_query.message.bot.send_photo(chat_id=callback_query.from_user.id, photo=event['img_url'], caption=text_message, parse_mode="HTML")
            else:
                await callback_query.message.bot.send_message(chat_id=callback_query.from_user.id, text=text_message, parse_mode="HTML")
    else:
        await callback_query.message.bot.send_message(chat_id=callback_query.from_user.id, text="Мероприятия не найдены.", parse_mode="HTML")

def register_new_holland_handlers(dp: Dispatcher):
    dp.callback_query.register(handle_new_holland, lambda c: c.data == "new_holland")
