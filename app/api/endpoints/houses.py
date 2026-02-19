from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Query
from app.schemas.house import HouseDetailSchema, HouseItemSchema
from typing import List, Optional, Literal
from app.api.deps import DBSessionDep
from app.crud.houses import get_active_houses, get_active_house


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

    houses = get_active_houses(session, min_price=min_price, max_price=max_price, order_by=order_by, order=order)

    return houses


@houses_router.get("/{house_id}", response_model=HouseDetailSchema)
async def get_house(session: DBSessionDep, house_id: int):
    house = get_active_house(session=session, house_id=house_id)

    if house is not None:
        return house

    raise HTTPException(status_code=404, detail=f"House {house_id} not found")
