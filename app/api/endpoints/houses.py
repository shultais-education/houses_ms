from fastapi import APIRouter
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

    return {"message": f"Дом не найден"}
