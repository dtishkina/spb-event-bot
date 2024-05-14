from aiogram import Bot, Dispatcher, Router
from aiogram.client.session.aiohttp import AiohttpSession
import asyncio
import aiohttp
from aiogram.filters.command import Command
from aiogram import types
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

API_TOKEN = '6369791900:AAHODgzc5Gnd1e7XC4tFuOv4Lq0w5XUI_kU'
# Инициализация сессии и бота
session = AiohttpSession()
bot = Bot(token=API_TOKEN, session=session)

# Создание роутера и диспетчера
router = Router()
dp = Dispatcher()
dp.include_router(router)
def get_inline_keyboard():
    # Создание объекта инлайн клавиатуры с явным указанием кнопок в конструкторе
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Новая Голландия", callback_data="new_holland")],
        [types.InlineKeyboardButton(text="Севкабель Порт", callback_data="sevcable_port")]
    ])
    return markup

@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    await message.answer(
        "Нажмите на одну из кнопок ниже, чтобы получить информацию о мероприятиях:",
        reply_markup=get_inline_keyboard()
    )

async def fetch_new_holland_events():
    URL = "https://www.newhollandsp.ru/events/all-events/"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            page_content = await response.text()

    soup = BeautifulSoup(page_content, "html.parser")
    events = soup.find_all("div", class_="item")  # Класс для поиска контейнеров мероприятий

    events_info = []
    for event in events:
        event_url = event.find("a", class_="event")["href"]
        event_url_full = f"https://www.newhollandsp.ru{event_url}" if event_url.startswith('/') else event_url

        img_tag = event.find("img", class_="img-responsive")
        img_url = img_tag["src"] if img_tag else None
        img_url_full = f"https://www.newhollandsp.ru{img_url}" if img_url and img_url.startswith('/') else img_url

        event_name = img_tag["alt"] if img_tag else "Название не указано"

        event_date_tag = event.find("span", class_="event-date")
        event_date = event_date_tag.text.strip() if event_date_tag else "Дата не указана"

        events_info.append({
            "name": event_name,
            "date": event_date,
            "img_url": img_url_full,
            "event_url": event_url_full
        })

    return events_info


    return events_info


@router.callback_query(lambda c: c.data == "new_holland")
async def handle_new_holland(callback_query: types.CallbackQuery):
    await callback_query.answer("Загружаем мероприятия Новой Голландии...")
    events_info = await fetch_new_holland_events()

    # Удаляем предыдущее сообщение с клавиатурой
    await callback_query.message.delete()

    if events_info:
        for event in events_info:
            text_message = f"{event['date']} - {event['name']}\n[Подробнее...]({event['event_url']})"
            # Если есть URL изображения, отправляем его вместе с текстом
            if event.get('img_url'):
                await bot.send_photo(chat_id=callback_query.from_user.id, photo=event['img_url'], caption=text_message,
                                     parse_mode="Markdown")
            else:
                await bot.send_message(chat_id=callback_query.from_user.id, text=text_message, parse_mode="Markdown")
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Мероприятия не найдены.")


async def fetch_sevcableport_events():
    URL = "https://sevcableport.ru/ru/afisha"
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            page_content = await response.text()

    soup = BeautifulSoup(page_content, "html.parser")
    cards = soup.find_all("a", class_="ActivityCard_card__3eBST")

    events_info = []
    for card in cards:
        body = card.find("div", class_="ActivityCard_body__2pEAx")
        if not body:
            continue

        event_type = body.find("span", class_="ActivityCard_tag__ZA8YN")
        event_title = body.find("h3", class_="ActivityCard_title__2AUzM")
        event_dates = body.find("span", class_="ActivityCard_decals__3NUGK")
        today_time_elements = body.find_all("span", class_="ActivityCard_date__2S1AS")
        venue = body.find("span", class_="ParentLabel_parent__qC-rf")
        img_tag = card.find("img", class_="ResponsivePicture_image__10h8-")

        event_info = {
            "type": event_type.get_text(strip=True) if event_type else "Тип не указан",
            "title": event_title.get_text(strip=True) if event_title else "Название не указано",
            "dates": event_dates.get_text(strip=True) if event_dates else "Дата не указана",
            "today_time": ", ".join([time.get_text(strip=True) for time in today_time_elements]),
            "venue": venue.get_text(strip=True) if venue else "Место проведения не указано",
            "img_url": img_tag["src"] if img_tag else None
        }
        events_info.append(event_info)

    return events_info


# Обработчик callback для Севкабель Порта
@router.callback_query(lambda c: c.data == "sevcable_port")
async def handle_sevcable_port(callback_query: types.CallbackQuery):
    await callback_query.answer("Загружаем мероприятия Севкабель Порта...")
    events_info = await fetch_sevcableport_events()

    await callback_query.message.delete()

    if events_info:
        for event in events_info:
            text_message = f"{event['dates']} - {event['title']}\nТип: {event['type']}\nМесто: {event['venue']}\n{event['today_time']}"
            if event.get('img_url'):
                await bot.send_photo(chat_id=callback_query.from_user.id, photo=event['img_url'], caption=text_message)
            else:
                await bot.send_message(chat_id=callback_query.from_user.id, text=text_message)
    else:
        await bot.send_message(chat_id=callback_query.from_user.id, text="Мероприятия не найдены.")


# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())