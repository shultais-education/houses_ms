from uuid import uuid4
from pathlib import Path
from datetime import datetime as dt
from app.core.config import settings

from app.models import House
from app.repositories.houses import HouseRepository
from app.services.cache import CacheService
from app.schemas.house import HouseCreateSchema, HouseUpdateSchema, HousePreviewSchema
from sqlalchemy import Sequence
from pydantic_core import ValidationError
# import aiofiles
import aioboto3


class HouseService:
    CACHE_TTL = 600
    PREVIEWS_PATH = Path("houses/previews")

    def __init__(self, repository: HouseRepository, cache: CacheService = None):
        self.repository = repository
        self.cache = cache

    @staticmethod
    def _house_key(house_id):
        return f"house:{house_id}"

    @staticmethod
    def _get_preview_filename(original_filename: str) -> Path:
        ext = Path(original_filename).suffix
        return Path(f"{uuid4()}{ext}")

    @staticmethod
    def _get_preview_dir() -> Path:
        date_path = Path(dt.now().strftime("%Y/%m/%d"))
        return HouseService.PREVIEWS_PATH / date_path

    @staticmethod
    def _get_preview_full_dir() -> Path:
        return settings.MEDIA_ROOT / HouseService._get_preview_dir()

    @staticmethod
    def _create_preview_full_dir():
        HouseService._get_preview_full_dir().mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _get_preview_path(filename: Path) -> Path:
        preview_dir = HouseService._get_preview_dir()
        return preview_dir / filename

    @staticmethod
    def _get_preview_full_path(filename: Path) -> Path:
        preview_full_dir = HouseService._get_preview_full_dir()
        return preview_full_dir / filename

    async def save_preview(self, house, file) -> House:
        HouseService._create_preview_full_dir()

        filename = HouseService._get_preview_filename(file.filename)
        preview_full_path = HouseService._get_preview_full_path(filename)

        # async with aiofiles.open(preview_full_path, "wb") as f:
        #     while chunk := await file.read(1024):
        #         await f.write(chunk)

        session = aioboto3.Session()
        async with session.client(
                "s3",
                endpoint_url=settings.S3_ENDPOINT,
                aws_access_key_id=settings.S3_ACCESS_KEY,
                aws_secret_access_key=settings.S3_SECRET_KEY,
                region_name=settings.S3_REGION
        ) as s3_client:
            content = await file.read()
            key = str(HouseService._get_preview_path(filename))

            await s3_client.put_object(Bucket=settings.S3_BUCKET, Key=key, Body=content)

        house = await self.repository.add_preview(house=house, preview=HousePreviewSchema(**{
            "preview": str(HouseService._get_preview_path(filename))
        }))

        await self._clear_house_cache(house_id=house.id)

        return house

    @staticmethod
    def build_house_from_schema(data: HouseCreateSchema) -> House:
        return House.model_validate(data)

    async def _clear_house_cache(self, house_id: int):
        await self.cache.delete(key=self._house_key(house_id))

    async def create_house(self, house: House) -> House:
        house.active = False
        return await self.repository.create_house(house=house)

    async def update_house(self, house: House, house_data: HouseUpdateSchema) -> House:
        house = await self.repository.update_house(house=house, house_data=house_data)
        await self._clear_house_cache(house_id=house.id)
        return house

    async def get_house_for_update(self, house_id: int) -> House:
        return await self.repository.get_house(house_id=house_id)

    async def get_house(self, house_id: int) -> House:
        # Запросить дом из кэша
        key = self._house_key(house_id)
        house = None

        if self.cache:
            house = await self.cache.get(key=key)

        if house:
            try:
                house = self.repository.model.model_validate(house)
                return house
            except ValidationError:
                ...

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
        order_by, order = self._get_ordering(order_by, order)
        return await self.repository.get_houses(filters=filters, order_by=order_by, order=order)

    async def get_active_houses(self, filters=None, order_by="id", order="asc") -> Sequence[House]:
        if filters is None:
            filters = []

        filters.append(House.active == True)
        order_by, order = self._get_ordering(order_by, order)

        return await self.repository.get_houses(filters=filters, order_by=order_by, order=order)

    async def get_active_houses_count(self, filters=None) -> int:
        if filters is None:
            filters = []

        filters.append(House.active == True)

        return await self.repository.count_houses(filters=filters)

    async def delete_house(self, house_id: int) -> None:
        await self.repository.delete_house(house_id=house_id)
        await self._clear_house_cache(house_id=house_id)

    @staticmethod
    def _get_ordering(order_by, order):
        if order_by is None and order is None:
            order_by, order = "quality_score", "desc"
        elif order_by is not None and order is None:
            order = "asc"
        elif order_by is None and order is not None:
            order_by = "id"

        return order_by, order
