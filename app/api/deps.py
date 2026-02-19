from sqlmodel import Session
from fastapi import Depends
from typing import Annotated, TypeAlias
from app.db.session import get_session


DBSessionDep: TypeAlias = Annotated[Session, Depends(get_session)]

