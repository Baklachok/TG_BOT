from string import punctuation

from aiogram import Router, types, Bot
from aiogram.filters import Command

from filters.chat_types import ChatTypeFilter

user_group_router = Router()
user_group_router.message.filter(ChatTypeFilter(['group', 'supergroup']))

restricted_words = {'хуй', 'пизда', 'жопа'}

@user_group_router.message(Command("admin"))
async def get_admins(message: types.Message, bot: Bot):
    chat_id = message.chat.id
    admins_list = await bot.get_chat_administrators(chat_id)

    admins_list = [
        member.user.id
        for member in admins_list
        if member.status == "creator" or member.status == "administrator"
    ]
    bot.my_admins_list = admins_list
    if message.from_user.id in admins_list:
        await message.delete()

def clean_text(text: str):
    return text.translate(str.maketrans('', '', punctuation))

@user_group_router.message()
async def cleaner(message: types.Message):
    if restricted_words.intersection(message.text.lower().split()):
        await message.answer(f"{message.from_user.first_name}, не матерись, дуралей")
        await message.delete()