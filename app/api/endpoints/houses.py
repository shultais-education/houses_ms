from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from app.data import houses_list
from app.schemas.house import HouseDetailSchema, HouseItemSchema
from typing import List, Optional, Literal
from app.api.deps import DBSessionDep
from sqlmodel import text


houses_router = APIRouter(prefix="/houses", tags=["houses"])


SortField = Literal["id", "price", "name"]
SortOrder= Literal["asc", "desc"]


@houses_router.get("/", response_model=List[HouseItemSchema])
async def get_houses(
        session: DBSessionDep,
        min_price: Optional[int] = Query(None, ge=0),
        max_price: Optional[int] = Query(None, ge=0),
        order_by: Optional[SortField] = Query("id"),
        order: Optional[SortOrder] = Query("asc")):

    print(session.exec(text("SELECT 1")))

    houses = [house for house in houses_list if house["active"]]

    if min_price is not None:
        houses = [house for house in houses if house["price"] >= min_price]

    if max_price is not None:
        houses = [house for house in houses if house["price"] <= max_price]

    # Сортировка
    reverse = order == "desc"
    houses.sort(key=lambda h: h[order_by], reverse=reverse)

    return houses


@houses_router.get("/{house_id}", response_model=HouseDetailSchema)
async def get_house(house_id: int):
    for house in houses_list:
        if house["id"] == house_id and house["active"]:
            return house

    raise HTTPException(status_code=404, detail=f"House {house_id} not found")
