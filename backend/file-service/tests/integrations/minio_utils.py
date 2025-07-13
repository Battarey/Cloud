import io
from minio_utils.minio_client import minio_client, MINIO_BUCKET

async def ensure_bucket():
    """Создать бакет, если не существует."""
    found = False
    for bucket in minio_client.list_buckets():
        if bucket.name == MINIO_BUCKET:
            found = True
            break
    if not found:
        minio_client.make_bucket(MINIO_BUCKET)

async def clear_bucket():
    """Удалить все объекты из бакета."""
    objects = minio_client.list_objects(MINIO_BUCKET, recursive=True)
    for obj in objects:
        minio_client.remove_object(MINIO_BUCKET, obj.object_name)

async def upload_test_file(storage_key: str, content: bytes = b"test", content_type: str = "text/plain"):
    minio_client.put_object(
        MINIO_BUCKET,
        storage_key,
        data=io.BytesIO(content),
        length=len(content),
        content_type=content_type
    )
