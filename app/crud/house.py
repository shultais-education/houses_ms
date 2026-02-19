from app.models import House
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, desc, asc
from typing import Sequence


async def get_filtered_active_houses(session: AsyncSession, filters=None, order_by="id", order="asc") -> Sequence[House]:
    stmt = select(House).where(House.active)

    if filters:
        stmt = filters.build_query(stmt)

    ordering = desc if order == "desc" else asc
    stmt = stmt.order_by(ordering(order_by))

    result = await session.execute(stmt)
    return result.scalars().all()


async def get_house(session: AsyncSession, house_id: int) -> House | None:
    stmt = select(House).where(House.active, House.id == house_id)
    result = await session.execute(stmt)
    return result.scalars().first()
