from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product
from database.orm_query import orm_add_product, orm_get_products, orm_delete_product, orm_get_product, \
    orm_update_product, orm_get_categories, orm_get_info_pages, orm_change_banner_image
from filters.chat_types import ChatTypeFilter, IsAdmin
from kbrd.inline import get_callback_btns
from kbrd.reply import get_keyboard

admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]), IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить товар",
    "Ассортимент",
    "Добавить/Изменить баннер",
    placeholder="Выберите действие",
    sizes=(2,),
)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    category = State()
    price = State()
    image = State()

    product_for_change = None

    texts = {
        'AddProduct:name': "Введите название заново",
        'AddProduct:description': "Введите описание заново",
        'AddProduct:category': 'Выберите категорию заново',
        'AddProduct:price': "Введите стоимость заново",
        'AddProduct:image': "Этот стейт последний, поэтому...",
    }

class AddBanner(StatesGroup):
    image = State()

@admin_router.message(Command("admin"))
async def admin_features(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Ассортимент")
async def admin_features(message: types.Message, session: AsyncSession):
    categories = await orm_get_categories(session)
    btns = {category.name: f'category_{category.id}' for category in categories}
    await message.answer('Выберите категорию', reply_markup=get_callback_btns(btns=btns))


@admin_router.callback_query(F.data.startswith("category_"))
async def starring_at_product(callback, session):
    category_id = callback.data.split("_")[-1]
    for product in await orm_get_products(session, int(category_id)):
        await callback.message.answer_photo(
            product.image,
            caption=f'<strong>{product.name}\
                    </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}',
            reply_markup=get_callback_btns(
                btns={
                    'Удалить': f'delete_{product.id}',
                    'Изменить': f'change_{product.id}',
                },
                sizes=(2,)
            ),
        )
    await callback.answer()
    await callback.message.answer('Список товаров:')

@admin_router.callback_query(F.data.startswith("delete_"))
async def delete_product_callback(callback, session):
    product_id = callback.data.split("_")[-1]
    await orm_delete_product(session, int(product_id))

    await callback.answer("Товар удален")
    await callback.message.answer("Товар удален!")

@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_product_callback(callback, state, session):
    product_id = callback.data.split("_")[-1]

    product_for_change = await orm_get_product(session, int(product_id))

    AddProduct.product_for_change = product_for_change

    await callback.answer()
    await callback.message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)

#Код ниже для машины состояний (FSM)

@admin_router.message(StateFilter(None), F.text == "Добавить товар")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название товара", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter("*"), Command("отмена"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter("*"), Command("назад"))
@admin_router.message(StateFilter("*"), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state == AddProduct.name:
        await message.answer("Предыдушего шага нет, или введите название товара или напишите 'отмена'")
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}")
            return
        previous = step


@admin_router.message(AddProduct.name, or_f(F.text, F.text == '.'))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(name=AddProduct.product_for_change.name)
    else:
        await state.update_data(name=message.text)
    await message.answer("Введите описание товара")
    await state.set_state(AddProduct.description)


@admin_router.message(AddProduct.description, or_f(F.text, F.text == '.'))
async def add_description(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == '.':
        await state.update_data(description=AddProduct.product_for_change.description)
    else:
        await state.update_data(description=message.text)

    categories = await orm_get_categories(session)
    btns = {category.name : str(category.id) for category in categories}
    await message.answer("Выберите категорию", reply_markup=get_callback_btns(btns=btns))
    await state.set_state(AddProduct.category)

@admin_router.callback_query(AddProduct.category)
async def category_choice(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    if int(callback.data) in [category.id for category in await orm_get_categories(session)]:
        await callback.answer()
        await state.update_data(category=callback.data)
        await callback.message.answer('Введите цену товара')
        await state.set_state(AddProduct.price)
    else:
        await callback.message.answer('Выберите категорию из кнопок.')
        await callback.answer()

@admin_router.message(AddProduct.category)
async def category_choice2(message: types.Message, state: FSMContext):
    await message.answer('Выберите категорию из кнопок.')

@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    if message.text == '.' and AddProduct.product_for_change:
        await state.update_data(price=AddProduct.product_for_change.price)
    else:
        try:
            float(message.text)
        except ValueError:
            await message.answer('Введите корректное значение цены')
            return

        await state.update_data(price=message.text)
    await message.answer("Загрузите изображение товара")
    await state.set_state(AddProduct.image)


@admin_router.message(AddProduct.image, or_f(F.photo, F.text == '.'))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    if message.text == '.':
        await state.update_data(image=AddProduct.product_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()

    if AddProduct.product_for_change:
        await orm_update_product(session, AddProduct.product_for_change.id, data)
    else:
        await orm_add_product(session, data)
    await message.answer("Товар добавлен/изменен", reply_markup=ADMIN_KB)
    await state.clear()

    AddProduct.product_for_change = None

@admin_router.message(StateFilter(None), F.text == 'Добавить/Изменить баннер')
async def add_image2(message: types.Message, state: FSMContext, session: AsyncSession):
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    await message.answer(f'Отправьте фото баннера.\nВ описании укажите для какой страницы:{','.join(pages_names)}')
    await state.set_state(AddBanner.image)

@admin_router.message(AddBanner.image, F.photo)
async def add_banner(message:types.Message, state: FSMContext, session: AsyncSession):
    image_id = message.photo[-1].file_id
    for_page = message.caption.strip()
    pages_names = [page.name for page in await orm_get_info_pages(session)]
    if for_page not in pages_names:
        await message.answer(f'Введите нормальное название страницы, например: {','.join(pages_names)}')
        return
    await orm_change_banner_image(session, for_page, image_id)
    await message.answer('Баннер добавлен/изменен.')
    await state.clear()
