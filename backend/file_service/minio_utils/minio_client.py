from minio import Minio
import os
import asyncio
from functools import partial

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)

# Асинхронные обёртки для часто используемых методов Minio
async def async_presigned_get_object(bucket_name, object_name, expires):
    loop = asyncio.get_running_loop()
    func = partial(minio_client.presigned_get_object, bucket_name, object_name, expires=expires)
    return await loop.run_in_executor(None, func)

async def async_put_object(bucket_name, object_name, data, length, content_type=None):
    loop = asyncio.get_running_loop()
    func = partial(minio_client.put_object, bucket_name, object_name, data, length, content_type=content_type)
    return await loop.run_in_executor(None, func)

async def async_get_object(bucket_name, object_name):
    loop = asyncio.get_running_loop()
    func = partial(minio_client.get_object, bucket_name, object_name)
    return await loop.run_in_executor(None, func)

async def async_remove_object(bucket_name, object_name):
    loop = asyncio.get_running_loop()
    func = partial(minio_client.remove_object, bucket_name, object_name)
    return await loop.run_in_executor(None, func)

async def async_bucket_exists(bucket_name):
    loop = asyncio.get_running_loop()
    func = partial(minio_client.bucket_exists, bucket_name)
    return await loop.run_in_executor(None, func)

async def async_make_bucket(bucket_name):
    loop = asyncio.get_running_loop()
    func = partial(minio_client.make_bucket, bucket_name)
    return await loop.run_in_executor(None, func)

async def async_list_buckets():
    loop = asyncio.get_running_loop()
    func = partial(minio_client.list_buckets)
    return await loop.run_in_executor(None, func)

async def async_list_objects(bucket_name, recursive=True):
    loop = asyncio.get_running_loop()
    func = partial(minio_client.list_objects, bucket_name, recursive=recursive)
    return await loop.run_in_executor(None, func)
