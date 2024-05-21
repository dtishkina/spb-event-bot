
import unittest
from unittest.mock import patch, AsyncMock
from aiogram import types, Bot, Dispatcher
import asyncio
from datetime import datetime

from handlers.common import send_welcome
from handlers.new_holland import handle_new_holland
from handlers.sevcable_port import handle_sevcable_port
from config import API_TOKEN


class TestBotHandlers(unittest.TestCase):

    def setUp(self):
        self.bot = Bot(token=API_TOKEN)
        self.dispatcher = Dispatcher()

        self.message = types.Message(
            message_id=1,
            from_user=types.User(id=1, is_bot=False, first_name='Test'),
            chat=types.Chat(id=1, type='private'),
            date=datetime.now(),
            text='/start'
        )

        self.callback_query_new_holland = types.CallbackQuery(
            id='1',
            from_user=types.User(id=1, is_bot=False, first_name='Test'),
            message=self.message,
            chat_instance='1',
            data='new_holland'
        )

        self.callback_query_sevcable_port = types.CallbackQuery(
            id='2',
            from_user=types.User(id=1, is_bot=False, first_name='Test'),
            message=self.message,
            chat_instance='1',
            data='sevcable_port'
        )

    @patch('handlers.common.types.Message.answer', new_callable=AsyncMock)
    async def test_send_welcome(self, mock_answer):
        await send_welcome(self.message)
        mock_answer.assert_awaited_once_with(
            "Нажмите на одну из кнопок ниже, чтобы получить информацию о мероприятиях:",
            reply_markup=types.InlineKeyboardMarkup(inline_keyboard=[
                [types.InlineKeyboardButton(text="Новая Голландия", callback_data="new_holland")],
                [types.InlineKeyboardButton(text="Севкабель Порт", callback_data="sevcable_port")]
            ])
        )

    @patch('handlers.new_holland.fetch_new_holland_events', new_callable=AsyncMock)
    @patch('handlers.new_holland.types.CallbackQuery.answer', new_callable=AsyncMock)
    @patch('handlers.new_holland.types.CallbackQuery.message.delete', new_callable=AsyncMock)
    async def test_handle_new_holland(self, mock_delete, mock_answer, mock_fetch_events):
        mock_fetch_events.return_value = [{
            "name": "Event 1",
            "date": "Date 1",
            "img_url": "https://example.com/img.jpg",
            "event_url": "https://example.com/event"
        }]

        with patch.object(self.bot, 'send_photo', new_callable=AsyncMock) as mock_send_photo:
            await handle_new_holland(self.callback_query_new_holland)
            mock_answer.assert_awaited_once()
            mock_delete.assert_awaited_once()
            mock_send_photo.assert_awaited_once_with(
                chat_id=self.callback_query_new_holland.from_user.id,
                photo="https://example.com/img.jpg",
                caption="Date 1 - Event 1\n<a href='https://example.com/event'>Подробнее...</a>",
                parse_mode="HTML"
            )



    @patch('handlers.sevcable_port.fetch_sevcableport_events', new_callable=AsyncMock)
    @patch('handlers.sevcable_port.types.CallbackQuery.answer', new_callable=AsyncMock)
    @patch('handlers.sevcable_port.types.CallbackQuery.message.delete', new_callable=AsyncMock)
    async def test_handle_sevcable_port(self, mock_delete, mock_answer, mock_fetch_events):
        mock_fetch_events.return_value = [{
        "type": "Type 1",
        "title": "Event 2",
        "dates": "Date 2",
        "today_time": "Time 2",
        "venue": "Venue 2",
        "img_url": "https://example.com/img2.jpg",
        "event_url": "https://example.com/event2"
        }]

        with patch.object(self.bot, 'send_photo', new_callable=AsyncMock) as mock_send_photo:
            await handle_sevcable_port(self.callback_query_sevcable_port)
            mock_answer.assert_awaited_once()
            mock_delete.assert_awaited_once()
            mock_send_photo.assert_awaited_once_with(
            chat_id=self.callback_query_sevcable_port.from_user.id,
            photo="https://example.com/img2.jpg",
            caption="Date 2 - Event 2\n<a href='https://example.com/event2'>Подробнее...</a>",
            parse_mode="HTML"
        )


if __name__ == 'main':
    unittest.main()
