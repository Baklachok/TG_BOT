import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv

load_dotenv()

bot = Bot(token=os.getenv("TG_TOKEN"))
dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer('Старт')

@dp.message()
async def echo(message: types.Message):
    text = message.text

    if text in ["Привет", "привет", "hi", "hello"]:
        await message.answer("И тебе салам")
    elif text in ["Пока", "пока", "пакеда", "До свидания"]:
        await message.answer("И тебе пока!")
    else:
        await message.answer(text)

async def main():
    await dp.start_polling(bot)
    
asyncio.run(main())
