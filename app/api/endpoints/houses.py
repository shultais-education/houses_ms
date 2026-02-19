from fastapi import APIRouter


houses_router = APIRouter()


@houses_router.get("/")
async def root():
    return {"message": "Hello World"}


@houses_router.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
