from aiogram import types

def get_inline_keyboard():
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="Новая Голландия", callback_data="new_holland")],
        [types.InlineKeyboardButton(text="Севкабель Порт", callback_data="sevcable_port")]
    ])
    return markup
