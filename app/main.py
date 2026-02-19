from fastapi import FastAPI
from app.api.endpoints.houses import houses_router


app = FastAPI()
app.include_router(houses_router)
