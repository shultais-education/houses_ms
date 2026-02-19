from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel
from typing import Type


class DBRepository:

    def __init__(self, model: Type[SQLModel], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_one(self, id_: int):
        ...

    async def get_many(self, filters=None, order_by="id", order="asc"):
        ...
