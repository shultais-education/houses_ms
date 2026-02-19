from typing import Annotated, TypeAlias

from app.schemas.filters import HouseFilters
from fastapi import Depends

HouseFiltersDep: TypeAlias = Annotated[HouseFilters, Depends()]
