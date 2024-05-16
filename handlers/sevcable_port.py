from aiogram import Dispatcher, types
from services.fetch_events import fetch_sevcableport_events
from utils.html_escape import escape_html

async def handle_sevcable_port(callback_query: types.CallbackQuery):
    await callback_query.answer("Загружаем мероприятия Севкабель Порта...")
    events_info = await fetch_sevcableport_events()

    await callback_query.message.delete()

    if events_info:
        for event in events_info:
            caption_text = f"{escape_html(event['dates'])} - {escape_html(event['title'])}"
            link_text = f'<a href="{event["event_url"]}">Подробнее...</a>'
            text_message = f"{caption_text}\n{link_text}"

            if event.get('img_url'):
                await callback_query.message.bot.send_photo(chat_id=callback_query.from_user.id, photo=event['img_url'], caption=text_message, parse_mode="HTML")
            else:
                await callback_query.message.bot.send_message(chat_id=callback_query.from_user.id, text=text_message, parse_mode="HTML")
    else:
        await callback_query.message.bot.send_message(chat_id=callback_query.from_user.id, text="Мероприятия не найдены.", parse_mode="HTML")

def register_sevcable_port_handlers(dp: Dispatcher):
    dp.callback_query.register(handle_sevcable_port, lambda c: c.data == "sevcable_port")
