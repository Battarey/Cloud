import io
from minio_utils.minio_client import (
    async_list_buckets, async_make_bucket, async_list_objects, async_remove_object, async_put_object, MINIO_BUCKET
)

async def ensure_bucket():
    """Создать бакет, если не существует."""
    found = False
    buckets = await async_list_buckets()
    for bucket in buckets:
        if bucket.name == MINIO_BUCKET:
            found = True
            break
    if not found:
        await async_make_bucket(MINIO_BUCKET)

async def clear_bucket():
    """Удалить все объекты из бакета."""
    objects = await async_list_objects(MINIO_BUCKET, recursive=True)
    for obj in objects:
        await async_remove_object(MINIO_BUCKET, obj.object_name)

async def upload_test_file(storage_key: str, content: bytes = b"test", content_type: str = "text/plain"):
    await async_put_object(
        MINIO_BUCKET,
        storage_key,
        data=io.BytesIO(content),
        length=len(content),
        content_type=content_type
    )
