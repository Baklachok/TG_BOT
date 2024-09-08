from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils import keyboard
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuCallBack(CallbackData, prefix="menu"):
    level: int
    menu_name: str
    category: int | None = None

def get_callback_btns(
        *,
        btns,
        sizes = (2,)):

        keyboard = InlineKeyboardBuilder()

        for text, data in btns.items():
            keyboard.add(InlineKeyboardButton(text=text, callback_data=data))

        return keyboard.adjust(*sizes).as_markup()


def get_user_main_btns(*, level, sizes=(2,)):
    keyboard = InlineKeyboardBuilder()
    btns = {
        'Товары 🍕': 'catalog',
        'Корзина 🛒': 'cart',
        'О нас ℹ': 'about',
        'Оплата 💰': 'payment',
        'Доставка 📬': 'shipping',
    }
    for text, menu_name in btns.items():
        if menu_name == 'catalog':
            keyboard.add(
                InlineKeyboardButton(text=text, callback_data=MenuCallBack(level=level+1, menu_name=menu_name).pack()))
        elif menu_name == 'cart':
            keyboard.add(
                InlineKeyboardButton(text=text, callback_data=MenuCallBack(level=3, menu_name=menu_name).pack()))
        else:
            keyboard.add(
                InlineKeyboardButton(text=text, callback_data=MenuCallBack(level=level, menu_name=menu_name).pack()))

    return keyboard.adjust(*sizes).as_markup()


def get_user_catalog_btns(*, level, categories, sizes=(2,)):
    keyboard = InlineKeyboardBuilder()

    keyboard.add(
        InlineKeyboardButton(text='Назад', callback_data=MenuCallBack(level=level-1, menu_name='main').pack()))
    keyboard.add(
        InlineKeyboardButton(text='Корзина 🛒', callback_data=MenuCallBack(level=3, menu_name='cart').pack()))

    for c in categories:
        keyboard.add(InlineKeyboardButton(text=c.name, callback_data=MenuCallBack(level=level + 1, menu_name=c.name,
                                                                                  category=c.id).pack()))

        return keyboard.adjust(*sizes).as_markup()
