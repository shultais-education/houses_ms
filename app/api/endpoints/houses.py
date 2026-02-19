from fastapi import APIRouter
from fastapi import HTTPException
from app.data import houses_list
from app.schemas.house import HouseDetailSchema, HouseItemSchema
from typing import List


houses_router = APIRouter(prefix="/houses", tags=["houses"])


@houses_router.get("/", response_model=List[HouseItemSchema])
async def get_houses():
    houses = [house for house in houses_list if house["active"]]
    return houses


@houses_router.get("/{house_id}", response_model=HouseDetailSchema)
async def get_house(house_id: int):
    for house in houses_list:
        if house["id"] == house_id:
            return house

    raise HTTPException(status_code=404, detail=f"House {house_id} not found")
