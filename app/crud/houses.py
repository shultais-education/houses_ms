from app.models import House
from sqlmodel import Session, select, desc, asc
from typing import Sequence


def get_active_houses(session: Session, min_price=None, max_price=None, order_by="id", order="asc") -> Sequence[House]:
    stmt = select(House).where(House.active)

    if min_price is not None:
        stmt = stmt.where(House.price >= min_price)

    if max_price is not None:
        stmt = stmt.where(House.price <= max_price)

    ordering = desc if order == "desc" else asc
    stmt = stmt.order_by(ordering(order_by))

    return session.exec(stmt).all()


def get_active_house(session: Session, house_id: int) -> House | None:
    return session.get(House, house_id)
