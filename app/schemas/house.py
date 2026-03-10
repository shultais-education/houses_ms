from typing import Optional
from pathlib import Path
from urllib.parse import urljoin
from pydantic import BaseModel, model_validator, computed_field
from pydantic import Field
from typing_extensions import Self
from app.core.config import settings


class HouseDetailSchema(BaseModel):
    id: int
    name: str = Field(description='Название дома')
    description: str = Field(description='Краткое описание')
    price: int = Field(description='Цена в рублях', examples=['5000', '10000'])
    preview: Optional[str] = Field(default="", description="Фото дома", exclude=True)

    text: str
    deposit: int | None
    square: int | None
    rooms: int
    bathrooms: int
    free_parking: bool
    pets_allowed: bool | None

    @computed_field
    @property
    def preview_url(self) -> str:
        if not self.preview:
            return ""

        preview = Path(self.preview)
        preview_dir = preview.parent
        filename = Path(f"{preview.stem}_1000x*{preview.suffix}")

        return urljoin(settings.MEDIA_URL, str(preview_dir / filename))


class HouseItemSchema(BaseModel):
    id: int
    name: str
    price: int | None = None
    preview: Optional[str] = Field(default="", description="Фото дома", exclude=True)

    @computed_field
    @property
    def preview_url(self) -> str:
        if not self.preview:
            return ""

        preview = Path(self.preview)
        preview_dir = preview.parent
        filename = Path(f"{preview.stem}_400x250{preview.suffix}")

        return urljoin(settings.MEDIA_URL, str(preview_dir / filename))


class HouseCreateSchema(BaseModel):
    name: str = Field(min_length=3, max_length=100)


class HouseUpdateSchema(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=100, description="Название")
    description: Optional[str] = Field(default=None, min_length=10, max_length=255, description="Описание")
    price: Optional[int] = Field(default=None, ge=0, description="Цена")
    text: Optional[str] = Field(default=None, min_length=100, description="Текст")
    deposit: Optional[int] = Field(default=None, ge=0, description="Депозит")
    square: Optional[int] = Field(default=None, gt=0, description="Площадь")
    rooms: Optional[int] = Field(default=None, gt=0, description="Комнат")
    bathrooms: Optional[int] = Field(default=None, gt=0, description="Ванных комнат")
    free_parking: Optional[bool] = Field(default=None, description="Бесплатная парковка")
    pets_allowed: Optional[bool] = Field(default=None, description="Разрешено с домашними животными")
    active: Optional[bool] = Field(default=None, description="Активный (доступен для бронирования)")

    @model_validator(mode='after')
    def check_deposit_le_price(self) -> Self:
        if self.price is not None and self.deposit is None:
            raise ValueError('При указании цены также нужно передавать и депозит')

        if self.price is None and self.deposit is not None:
            raise ValueError('При указании депозита также нужно передавать и цену')

        if self.deposit is not None and self.deposit > self.price:
            raise ValueError('Депозит не может быть больше цены')

        return self

    @model_validator(mode='after')
    def check_rooms(self) -> Self:
        if (self.bathrooms is not None and self.rooms is not None) and self.bathrooms > self.rooms:
            raise ValueError('Количество ванных комнат не может быть больше количества комнат.')

        return self


class HousePreviewSchema(BaseModel):
    preview: Optional[str] = Field(default=None)
