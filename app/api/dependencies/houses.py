from typing import Annotated, TypeAlias
from app.models.house import House
from app.repositories.houses import HouseRepository
from app.schemas.filters import HouseFilters
from app.services.houses import HouseService
from fastapi import Depends
from app.api.dependencies.database import DBSessionDep
from app.api.dependencies.cache import CacheServiceDep


def get_house_repository(session: DBSessionDep) -> HouseRepository:
    return HouseRepository(session=session, model=House)


HouseFiltersDep: TypeAlias = Annotated[HouseFilters, Depends()]
HouseRepositoryDep: TypeAlias = Annotated[HouseRepository, Depends(get_house_repository)]


def get_house_service(repository: HouseRepositoryDep, cache: CacheServiceDep) -> HouseService:
    return HouseService(repository=repository, cache=cache)


HouseServiceDep: TypeAlias = Annotated[HouseService, Depends(get_house_service)]
