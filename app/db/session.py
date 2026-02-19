from sqlmodel import create_engine, Session
from app.core.config import settings
from typing import Generator

engine = create_engine(settings.database_url, echo=settings.DB_ECHO)


def get_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session
