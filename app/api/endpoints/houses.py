from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from app.schemas.house import HouseDetailSchema, HouseItemSchema, HouseCreateSchema
from typing import List, Optional, Literal, Union
from app.api.dependencies.houses import HouseFiltersDep, HouseServiceDep
from starlette import status

houses_router = APIRouter(prefix="/houses", tags=["houses"])


SortField = Literal["id", "price", "name"]
SortOrder = Literal["asc", "desc"]


@houses_router.get("", response_model=List[HouseItemSchema], summary="Возвращает дома", description="Возвращает список активных домов")
async def get_houses(
        house_service: HouseServiceDep,
        filters: HouseFiltersDep,
        order_by: Union[Optional[SortField], None] = Query(None, title="Поля сортировки", description="Допустимые значения: id, price, name"),
        order: Union[Optional[SortOrder], None] = Query(None, title="Направление сортировки", description="Допустимые значения: asc, desc")
    ):

    houses = await house_service.get_active_houses(filters=filters.where_conditions, order_by=order_by, order=order)
    return houses


@houses_router.post("", response_model=HouseDetailSchema, summary="Создает дом")
async def create_houses(house_service: HouseServiceDep, house_data: HouseCreateSchema):
    house = house_service.build_house_from_schema(data=house_data)
    house = await house_service.create_house(house=house)
    return house


@houses_router.get("/{house_id}", response_model=HouseDetailSchema, summary="Возвращает дом")
async def get_house(house_service: HouseServiceDep, house_id: int):
    """
    Возвращает подробную информацию о доме:
       - **id**: идентификатор
       - **name**: название дома
       - **description**: короткое описание
       - **price**: цена дома в рублях
    """
    house = await house_service.get_active_house(house_id=house_id)

    if not house:
        raise HTTPException(status_code=404, detail=f"House {house_id} not found")

    return house


@houses_router.delete(
    "/{house_id}",
    summary="Удаляет дом",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={404: {'description': 'Дом не найден'}}
)
async def delete_house(house_service: HouseServiceDep, house_id: int):
    house = await house_service.get_active_house(house_id=house_id)

    if not house:
        raise HTTPException(status_code=404, detail=f"Дом {house_id} не найден")

    await house_service.delete_house(house_id=house_id)
    return None
