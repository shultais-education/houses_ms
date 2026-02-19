from sqlmodel import SQLModel, Field
import sqlalchemy as sa


class House(SQLModel, table=True):
    __tablename__ = "houses"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str = Field(default="")
    price: int = Field(default=0, index=True)
    active: bool = Field(default=True, index=True)

    square: int | None = Field(default=None)
    rooms: int | None = Field(default=1)
    bathrooms: int | None = Field(default=1, nullable=True)
    free_parking: bool = Field(
        default=False,
        sa_column=sa.Column(sa.Boolean, server_default=sa.text("FALSE"), nullable=False))
