from fastapi import FastAPI
from app.api.endpoints.houses import houses_router
from contextlib import asynccontextmanager
from app.models import *
from app.db.init import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield
    print("Завершение")


app = FastAPI(lifespan=lifespan, title="API домов", description="Микросервис для управления домами")
app.include_router(houses_router)
