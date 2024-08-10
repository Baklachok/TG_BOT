from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Product


async def orm_add_product(session, data):
    obj = Product(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image=data['image']
    )
    session.add(obj)
    await session.commit()

async def orm_get_products(session):
    query = select(Product)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_update_product(session, product_id, data):
    query = update(Product).where(Product.id == product_id).values(
        name=data['name'],
        description=data['description'],
        price=float(data['price']),
        image=data['image']
    )
    await session.execute(query)
    await session.commit()

async def orm_delete_product(session, product_id):
    query = delete(Product).where(Product.id == product_id)
    await session.execute(query)
    await session.commit()
