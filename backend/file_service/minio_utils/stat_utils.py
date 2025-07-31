import asyncio
from functools import partial
from minio_utils.minio_client import minio_client, MINIO_BUCKET

async def async_stat_object(object_name):
    loop = asyncio.get_running_loop()
    func = partial(minio_client.stat_object, MINIO_BUCKET, object_name)
    return await loop.run_in_executor(None, func)
