import asyncio
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from common.bot_cmd_list import private
from handlers.admin_private import admin_router
from handlers.user_group import user_group_router
from handlers.user_private import user_private_router

load_dotenv()

ALLOWED_UPDATES = ["message, edited_message"]

bot = Bot(token=os.getenv("TG_TOKEN"))
bot.my_admins_list = []

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
    
asyncio.run(main())
