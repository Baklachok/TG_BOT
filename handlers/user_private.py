from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, or_f

from filters.chat_types import ChatTypeFilter
from kbrd import reply

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        'Старт',
        reply_markup=reply.get_keyboard(
            "Меню",
            "О магазине",
            "Варианты оплаты",
            "Варианты доставки",
            placeholder="Что вас интересует?",
            sizes=(2, 2)
        )
    )

@user_private_router.message(or_f(Command("menu"), (F.text.lower() == "меню")))
async def menu_cmd(message: types.Message):
    await message.answer('Вот меню:')

@user_private_router.message(F.text.lower() == 'магия')
@user_private_router.message(F.text.lower().contains('магия'))
async def menu_cmd(message: types.Message):
    await message.answer('Это магический фильтр')

