import asyncio
from functools import partial
from minio_utils.minio_client import minio_client, MINIO_BUCKET

async def async_create_multipart_upload(object_name, content_type=None):
    loop = asyncio.get_running_loop()
    func = partial(minio_client._create_multipart_upload, MINIO_BUCKET, object_name, None)
    return await loop.run_in_executor(None, func)

async def async_upload_part(object_name, upload_id, part_number, data, length):
    loop = asyncio.get_running_loop()
    func = partial(minio_client._upload_part, MINIO_BUCKET, object_name, upload_id, part_number, data, length)
    return await loop.run_in_executor(None, func)

async def async_complete_multipart_upload(object_name, upload_id, parts):
    loop = asyncio.get_running_loop()
    func = partial(minio_client._complete_multipart_upload, MINIO_BUCKET, object_name, upload_id, parts)
    return await loop.run_in_executor(None, func)

async def async_abort_multipart_upload(object_name, upload_id):
    loop = asyncio.get_running_loop()
    func = partial(minio_client._abort_multipart_upload, MINIO_BUCKET, object_name, upload_id)
    return await loop.run_in_executor(None, func)
