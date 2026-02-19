from pydantic import BaseModel


class HouseFullSchema(BaseModel):
    id: int
    name: str
    description: str
    price: int
    active: bool


class HouseDetailSchema(BaseModel):
    id: int
    name: str
    description: str
    price: int


class HouseItemSchema(BaseModel):
    id: int
    name: str
    price: int | None = None

