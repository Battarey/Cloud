from fastapi import HTTPException
from datetime import timedelta

async def generate_presigned_url(bucket_name: str, object_name: str, expires: int = 10800) -> str:
    try:
        from minio_utils.minio_client import minio_client
        url = minio_client.presigned_get_object(
            bucket_name,
            object_name,
            expires=timedelta(seconds=expires)
        )
        return url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка генерации ссылки: {str(e)}")
