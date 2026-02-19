from fastapi import APIRouter


houses_router = APIRouter()


@houses_router.get("/houses")
async def houses():
    return {"message": "Вывод домов"}


@houses_router.get("/houses/{house_id}")
async def house_detail(house_id: int):
    return {"message": f"Вывод дома {house_id}"}
