from app.models import House
from sqlmodel import Session, select
from typing import Sequence


def get_active_houses(session: Session) -> Sequence[House]:
    stmt = select(House).where(House.active)
    return session.exec(stmt).all()


def get_active_house(session: Session, house_id: int) -> House | None:
    return session.get(House, house_id)
