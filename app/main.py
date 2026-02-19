from fastapi import FastAPI
from app.api.endpoints.houses import houses_router
from contextlib import asynccontextmanager
from app.db.session import async_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Начало")

    yield
    async_engine.dispose()


app = FastAPI(lifespan=lifespan, title="API домов", description="Микросервис для управления домами")
app.include_router(houses_router)
