from sqlmodel import SQLModel
from app.db.session import engine

def create_tables():
    SQLModel.metadata.create_all(engine)
