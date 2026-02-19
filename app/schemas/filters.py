from typing import Optional
from fastapi import Query
from dataclasses import dataclass


@dataclass
class HouseFilters:
    search: Optional[str] = Query(None, min_length=3, title="Поиск по названию")
    min_price: Optional[int] = Query(None, ge=0, title="Минимальная цена")
    max_price: Optional[int] = Query(None, ge=0, title="Максимальная цена")
