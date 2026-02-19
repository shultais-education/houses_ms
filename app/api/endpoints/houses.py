from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from app.schemas.house import HouseDetailSchema, HouseItemSchema
from typing import List, Optional, Literal
from app.api.dependencies.houses import HouseFiltersDep, HouseServiceDep
from app.api.dependencies.cache import CacheServiceDep


houses_router = APIRouter(prefix="/houses", tags=["houses"])


SortField = Literal["id", "price", "name"]
SortOrder = Literal["asc", "desc"]


@houses_router.get("", response_model=List[HouseItemSchema], summary="Возвращает дома", description="Возвращает список активных домов")
async def get_houses(
        house_service: HouseServiceDep,
        cache: CacheServiceDep,
        filters: HouseFiltersDep,
        order_by: Optional[SortField] = Query("id", title="Поля сортировки", description="Допустимые значения: id, price, name"),
        order: Optional[SortOrder] = Query("asc", title="Направление сортировки", description="Допустимые значения: asc, desc")
    ):

    await cache.set(key="TEST-50", value="TEST VALUE-60", ttl=60)
    houses = await house_service.get_houses(filters=filters, order_by=order_by, order=order)
    return houses


@houses_router.get("/{house_id}", response_model=HouseDetailSchema, summary="Возвращает дом")
async def get_house(
        cache: CacheServiceDep,
        house_service: HouseServiceDep, house_id: int):
    """
    Возвращает подробную информацию о доме:
       - **id**: идентификатор
       - **name**: название дома
       - **description**: короткое описание
       - **price**: цена дома в рублях
    """
    house = await house_service.get_house(house_id=house_id)
    value = await cache.get(key="TEST-50")

    if not house:
        raise HTTPException(status_code=404, detail=f"House {house_id} not found")

    return house
