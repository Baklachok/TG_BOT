import asyncio
import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()

from middlewares.db import DataBaseSession
from database.engine import create_db, drop_db, session_maker
from handlers.admin_private import admin_router
from handlers.user_group import user_group_router
from handlers.user_private import user_private_router

ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]

bot = Bot(token=os.getenv("TG_TOKEN"))
bot.my_admins_list = []

dp = Dispatcher()

dp.include_router(user_private_router)
dp.include_router(user_group_router)
dp.include_router(admin_router)

async def on_startup(bot):

    # await drop_db()

    await create_db()

async def on_shutdown(bot):
    print('бот лег')

async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.update.middleware(DataBaseSession(session_pool=session_maker))

    await bot.delete_webhook(drop_pending_updates=True)
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    
asyncio.run(main())
