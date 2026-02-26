from pydantic import BaseModel, Field
from typing import Optional


class HouseDetailSchema(BaseModel):
    id: int
    name: str = Field(description='Название дома')
    description: str = Field(description='Краткое описание')
    price: int = Field(description='Цена в рублях', examples=['5000', '10000'])

    text: str
    deposit: int | None
    square: int | None
    rooms: int
    bathrooms: int
    free_parking: bool
    pets_allowed: bool | None


class HouseItemSchema(BaseModel):
    id: int
    name: str
    price: int | None = None


class HouseCreateSchema(BaseModel):
    name: str = Field(min_length=3, max_length=100)


class HouseUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100)
    description: Optional[str] = None
    price: Optional[int] = None
    text: Optional[str] = None
    deposit: Optional[int] = None
    square: Optional[int] = None
    rooms: Optional[int] = None
    bathrooms: Optional[int] = None
    free_parking: Optional[bool] = None
    pets_allowed: Optional[bool] = None
    active: Optional[bool] = None
