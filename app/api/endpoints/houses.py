from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from app.data import houses_list
from app.schemas.house import HouseDetailSchema, HouseItemSchema
from typing import List, Optional, Literal
from app.api.deps import DBSessionDep
from app.crud.houses import get_active_houses



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

    houses = get_active_houses(session)

    return houses


@houses_router.get("/{house_id}", response_model=HouseDetailSchema)
async def get_house(house_id: int):
    for house in houses_list:
        if house["id"] == house_id and house["active"]:
            return house

    raise HTTPException(status_code=404, detail=f"House {house_id} not found")
