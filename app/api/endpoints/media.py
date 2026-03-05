from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
from app.core.config import settings


media_router = APIRouter(prefix="/media", tags=["media"])


@media_router.get("/{filename:path}", summary="Возвращает media файлы")
async def get_media(filename: str):
    path = settings.MEDIA_ROOT / Path(filename)

    if not path.exists():
        raise HTTPException(status_code=404, detail=f"Файл {filename} не найден")

    return FileResponse(path)
