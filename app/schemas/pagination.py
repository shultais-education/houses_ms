from dataclasses import dataclass
from typing import Optional, TypeVar, Generic

from fastapi import Query
from pydantic import BaseModel


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    page_size: int
    pages: int


@dataclass
class PaginatorFilters:
    page: Optional[int] = Query(default=1, ge=1, title="Номер страницы")
    page_size: Optional[int] = Query(default=10, ge=1, le=100, title="Объектов на страницу")
