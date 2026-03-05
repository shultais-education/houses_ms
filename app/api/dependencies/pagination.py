from typing import Annotated, TypeAlias

from app.schemas.pagination import PaginatorFilters
from fastapi import Depends

PaginatorFiltersDep: TypeAlias = Annotated[PaginatorFilters, Depends()]
