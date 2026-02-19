from fastapi import APIRouter
from fastapi import HTTPException
from app.data import houses_list

houses_router = APIRouter(prefix="/houses", tags=["houses"])


@houses_router.get("/")
async def houses():
    return houses_list


@houses_router.get("/{house_id}")
async def house_detail(house_id: int):
    for house in houses_list:
        if house["id"] == house_id:
            return house

    raise HTTPException(status_code=404, detail=f"House {house_id} not found")
