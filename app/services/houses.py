from app.models import House
from app.repositories.houses import HouseRepository
from app.services.cache import CacheService
from sqlalchemy import Sequence


class HouseService:
    CACHE_TTL = 60

    def __init__(self, repository: HouseRepository, cache: CacheService):
        self.repository = repository
        self.cache = cache

    async def get_house(self, house_id: int) -> House:
        return await self.repository.get_house(house_id=house_id)

    async def get_active_house(self, house_id: int) -> House:
        # Фильтр по активному дому
        return await self.repository.get_house(house_id=house_id)

    async def get_houses(self, filters=None, order_by="id", order="asc") -> Sequence[House]:
        return await self.repository.get_houses(filters=filters, order_by=order_by, order=order)

    async def get_active_houses(self, filters=None, order_by="id", order="asc") -> Sequence[House]:
        # Фильтр по активным домам
        return await self.repository.get_houses(filters=filters, order_by=order_by, order=order)
