from fastapi import APIRouter, Query
from .service import generate_presigned_url

router = APIRouter()

@router.get(
    "/generate-link",
    description="Генерирует временную ссылку для скачивания файла (срок жизни 3 часа)"
)
async def get_download_link(bucket: str = Query(...), object_name: str = Query(...)):
    url = await generate_presigned_url(bucket, object_name, expires=10800)
    return {"url": url}
