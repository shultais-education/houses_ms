from app.services.cache import CacheService
from fastapi import Depends
from typing import Annotated, TypeAlias
from fastapi import Request


def get_cache_service(request: Request) -> CacheService:
    return CacheService(redis_client=request.app.state.redis)


CacheServiceDep: TypeAlias = Annotated[CacheService, Depends(get_cache_service)]
