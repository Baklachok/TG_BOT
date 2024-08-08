from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command

from filters.chat_types import ChatTypeFilter

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(['private']))

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Старт')

@user_private_router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    await message.answer('Вот меню:')

@user_private_router.message(F.text.lower() == 'магия')
@user_private_router.message(F.text.lower().contains('магия'))
async def menu_cmd(message: types.Message):
    await message.answer('Это магический фильтр')

