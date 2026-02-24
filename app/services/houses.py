from app.models import House
from app.repositories.houses import HouseRepository
from app.services.cache import CacheService
from sqlalchemy import Sequence


class HouseService:
    CACHE_TTL = 60

    def __init__(self, repository: HouseRepository, cache: CacheService = None):
        self.repository = repository
        self.cache = cache

    @staticmethod
    def _house_key(house_id):
        return f"house:{house_id}"

    async def get_house(self, house_id: int) -> House:
        # Запросить дом из кэша
        key = self._house_key(house_id)
        house = None

        if self.cache:
            house = await self.cache.get(key=key)

        if house:
            house = self.repository.model.model_validate(house)
            return house

        house = await self.repository.get_house(house_id=house_id)

        if self.cache and house:
            await self.cache.set(key=key, value=house.model_dump(), ttl=self.CACHE_TTL)

        return house

    async def get_active_house(self, house_id: int) -> House | None:
        # Фильтр по активному дому
        house = await self.get_house(house_id=house_id)

        if house and house.active:
            return house

        return None

    async def get_houses(self, filters=None, order_by="id", order="asc") -> Sequence[House]:
        return await self.repository.get_houses(filters=filters, order_by=order_by, order=order)

    async def get_active_houses(self, filters=None, order_by="id", order="asc") -> Sequence[House]:
        # Фильтр по активным домам
        return await self.repository.get_houses(filters=filters, order_by=order_by, order=order)

    async def delete_house(self, house_id: int) -> None:
        await self.repository.delete_house(house_id=house_id)
