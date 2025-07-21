from fastapi import HTTPException
from datetime import timedelta
from minio_utils.minio_client import async_presigned_get_object

async def generate_presigned_url(
    bucket_name: str,
    object_name: str,
    expires: int = 10800,
    presigned_get_object_func=async_presigned_get_object
) -> str:
    import traceback
    try:
        url = await presigned_get_object_func(
            bucket_name,
            object_name,
            expires=timedelta(seconds=expires)
        )
        return url
    except Exception as e:
        tb = traceback.format_exc()
        print(f"[generate_presigned_url] Exception: {e}\nTraceback:\n{tb}")
        raise HTTPException(status_code=500, detail=f"Ошибка генерации ссылки: {str(e)}")
