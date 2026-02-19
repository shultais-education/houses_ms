from app.models import House
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc, asc, or_
from typing import Sequence


async def get_filtered_active_houses(session: AsyncSession, filters=None, order_by="id", order="asc") -> Sequence[House]:
    stmt = select(House).where(House.active)

    if filters.search:
        # stmt = stmt.where(House.description.icontains(search) | House.name.icontains(search))
        stmt = stmt.where(or_(House.description.icontains(filters.search), House.name.icontains(filters.search)))

    if filters.min_price is not None:
        stmt = stmt.where(House.price >= filters.min_price)

    if filters.max_price is not None:
        stmt = stmt.where(House.price <= filters.max_price)

    ordering = desc if order == "desc" else asc
    stmt = stmt.order_by(ordering(order_by))

    result = await session.execute(stmt)
    return result.scalars().all()


async def get_house(session: AsyncSession, house_id: int) -> House | None:
    stmt = select(House).where(House.active, House.id == house_id)
    result = await session.execute(stmt)
    return result.scalars().first()
