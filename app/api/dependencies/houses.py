from typing import Annotated, TypeAlias
from app.models.house import House
from app.repositories.houses import HouseRepository
from app.schemas.filters import HouseFilters
from fastapi import Depends
from app.api.dependencies.database import DBSessionDep


def get_house_repository(session: DBSessionDep) -> HouseRepository:
    return HouseRepository(session=session, model=House)


HouseFiltersDep: TypeAlias = Annotated[HouseFilters, Depends()]
HouseRepositoryDep: TypeAlias = Annotated[HouseRepository, Depends(get_house_repository)]
