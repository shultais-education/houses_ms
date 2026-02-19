from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from sqlmodel import select, desc, asc


class DBRepository:

    def __init__(self, model: Type[SQLModel], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_one(self, id_: int):
        stmt = select(self.model).where(self.model.id == id_)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def get_many(self, filters=None, order_by="id", order="asc"):
        stmt = select(self.model)

        if filters:
            stmt = filters.build_query(stmt)

        ordering = desc if order == "desc" else asc
        stmt = stmt.order_by(ordering(order_by))

        result = await self.session.execute(stmt)
        return result.scalars().all()
