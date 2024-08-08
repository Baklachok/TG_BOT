from aiogram import types, Router
from aiogram.filters import CommandStart, Command

user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Старт')

@user_private_router.message(Command("menu"))
async def menu_cmd(message: types.Message):
    await message.answer('Вот меню:')


@user_private_router.message()
async def echo(message: types.Message):
    text = message.text

    if text in ["Привет", "привет", "hi", "hello"]:
        await message.answer("И тебе салам")
    elif text in ["Пока", "пока", "пакеда", "До свидания"]:
        await message.answer("И тебе пока!")
    else:
        await message.answer(text)