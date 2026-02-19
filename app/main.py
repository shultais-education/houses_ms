from fastapi import FastAPI
from app.api.endpoints.houses import houses_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Начало")
    yield
    print("Завершение")


app = FastAPI(lifespan=lifespan, title="API домов", description="Микросервис для управления домами")
app.include_router(houses_router)
