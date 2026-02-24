from app.models import House
from app.repositories.db import DBRepository
from sqlalchemy import Sequence


class HouseRepository(DBRepository):

    async def get_house(self, house_id: int) -> House:
        return await self.get_one(id_=house_id)

    async def get_houses(self, filters=None, order_by="id", order="asc") -> Sequence[House]:
        return await self.get_many(filters=filters, order_by=order_by, order=order)

    async def delete_house(self, house_id: int) -> None:
        await self.delete_one(id_=house_id)
