from fastapi import APIRouter, Query
from .service import generate_presigned_url

from minio_utils.minio_client import async_presigned_get_object
from fastapi import Depends

def get_presigned_get_object():
    return async_presigned_get_object

router = APIRouter()

@router.get(
    "/generate-link",
    description="Генерирует временную ссылку для скачивания файла (срок жизни 3 часа)"
)
async def get_download_link(
    bucket: str = Query(...),
    object_name: str = Query(...),
    presigned_get_object_func=Depends(get_presigned_get_object)
):
    url = await generate_presigned_url(
        bucket,
        object_name,
        expires=10800,
        presigned_get_object_func=presigned_get_object_func
    )
    return {"url": url}
