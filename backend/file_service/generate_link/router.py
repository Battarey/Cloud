from fastapi import APIRouter, Query, Response, Depends
from .service import generate_presigned_url
from minio_utils.minio_client import async_presigned_get_object
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session
from download_file.service import get_file_for_download

router = APIRouter()

def get_presigned_get_object():
    return async_presigned_get_object

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

@router.get(
    "/generate-link/direct/{file_id}/{user_id}",
    description="Скачивание расшифрованного файла по прямой ссылке (без авторизации)"
)
async def direct_download_file(
    file_id: str,
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
    get_object_func=None
):
    if get_object_func is None:
        file_data, file = await get_file_for_download(file_id, user_id, session)
    else:
        file_data, file = await get_file_for_download(file_id, user_id, session, get_object_func=get_object_func)
    return Response(content=file_data, media_type=file.content_type, headers={
        "Content-Disposition": f"attachment; filename={file.filename}"
    })
