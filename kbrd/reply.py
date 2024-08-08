from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder

start_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Меню'),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder='Что вас интересует?'
)

del_kbd = ReplyKeyboardRemove()

start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(KeyboardButton(text='Меню'))
start_kb2.adjust(1, 1)

start_kb3 = ReplyKeyboardBuilder()
start_kb3.attach((start_kb2))
start_kb3.row(KeyboardButton(text="Оставить отзыв"))