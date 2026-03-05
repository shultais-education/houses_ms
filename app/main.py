from fastapi import FastAPI
from redis.asyncio import Redis
from app.api.endpoints.houses import houses_router
from app.api.endpoints.media import media_router
from contextlib import asynccontextmanager
from app.db.session import async_engine
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = await Redis.from_url(str(settings.redis_url), encoding="utf-8", decode_responses=True)
    app.state.redis = redis_client

    yield

    await async_engine.dispose()
    await redis_client.close()


app = FastAPI(lifespan=lifespan, title="API домов", description="Микросервис для управления домами")
app.include_router(houses_router)
app.include_router(media_router)
