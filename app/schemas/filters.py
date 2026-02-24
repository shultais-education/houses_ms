from dataclasses import dataclass
from typing import Optional

from app.models import House
from fastapi import Query
from sqlmodel import or_


@dataclass
class HouseFilters:
    search: Optional[str] = Query(None, min_length=3, title="Поиск по названию")
    min_price: Optional[int] = Query(None, ge=0, title="Минимальная цена")
    max_price: Optional[int] = Query(None, ge=0, title="Максимальная цена")
    pets: Optional[bool] = Query(None, title="Разрешено с домашними животными")

    def build_query(self, base_query):
        query = base_query

        if self.pets is not None:
            query = query.where(House.pets_allowed == self.pets)

        if self.search:
            query = query.where(or_(House.description.icontains(self.search), House.name.icontains(self.search)))

        if self.min_price is not None:
            query = query.where(House.price >= self.min_price)

        if self.max_price is not None:
            query = query.where(House.price <= self.max_price)

        return query

