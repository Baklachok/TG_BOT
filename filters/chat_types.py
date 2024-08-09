from aiogram import types, Bot
from aiogram.filters import Filter


class ChatTypeFilter(Filter):
    def __init__(self, chat_types):
        self.chat_types = chat_types

    async def __call__(self, message):
        return message.chat.type in self.chat_types

class IsAdmin(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: types.Message, bot: Bot) -> bool:
        return message.from_user.id in bot.my_admins_list
