from pydantic import BaseModel, Field


class HouseFullSchema(BaseModel):
    id: int
    name: str
    description: str
    price: int
    active: bool


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
