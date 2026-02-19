from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from app.data import houses_list
from app.schemas.house import HouseDetailSchema, HouseItemSchema
from typing import List, Optional


houses_router = APIRouter(prefix="/houses", tags=["houses"])


@houses_router.get("/", response_model=List[HouseItemSchema])
async def get_houses(
        min_price: Optional[int] = Query(None),
        max_price: Optional[int] = Query(None)):

    houses = [house for house in houses_list if house["active"]]

    if min_price is not None:
        houses = [house for house in houses if house["price"] >= min_price]

    if max_price is not None:
        houses = [house for house in houses if house["price"] <= max_price]

    return houses


@houses_router.get("/{house_id}", response_model=HouseDetailSchema)
async def get_house(house_id: int):
    for house in houses_list:
        if house["id"] == house_id:
            return house

    raise HTTPException(status_code=404, detail=f"House {house_id} not found")
