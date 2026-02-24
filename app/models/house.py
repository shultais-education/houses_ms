from sqlmodel import SQLModel, Field
import sqlalchemy as sa


class House(SQLModel, table=True):
    __tablename__ = "houses"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(
        sa_column=sa.Column(sa.String, nullable=False, index=True)
    )
    description: str = Field(
        default="",
        sa_column=sa.Column(sa.String, server_default=sa.text("''"), nullable=False)
    )
    price: int = Field(
        default=0,
        sa_column=sa.Column(sa.Integer, server_default=sa.text("0"), nullable=False, index=True)
    )
    active: bool = Field(
        default=False,
        sa_column=sa.Column(sa.Boolean, server_default=sa.text("FALSE"), nullable=False, index=True)
    )

    # Дополнительные атрибуты
    square: int = Field(
        default=None,
        sa_column=sa.Column(sa.Integer, nullable=True)
    )
    rooms: int = Field(
        default=1,
        sa_column=sa.Column(sa.Integer, server_default=sa.text("1"), nullable=False)
    )
    bathrooms: int = Field(
        default=1,
        sa_column=sa.Column(sa.Integer, server_default=sa.text("1"), nullable=False)
    )
    free_parking: bool = Field(
        default=False,
        sa_column=sa.Column(sa.Boolean, server_default=sa.text("FALSE"), nullable=False))
