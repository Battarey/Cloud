from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from schemas.file import FileRead
from minio_utils.minio_client import async_put_object, MINIO_BUCKET, minio_client
from statistics.utils import update_user_stat
import uuid
from fastapi import HTTPException
import re
from sqlalchemy.future import select
import io
from typing import AsyncGenerator
from minio_utils.multipart_utils import async_create_multipart_upload, async_upload_part, async_complete_multipart_upload, async_abort_multipart_upload
from minio_utils.stat_utils import async_stat_object
from virus_scan.service import scan_file_with_clamav
import os
from fastapi import UploadFile
import json
import time

async def scan_file_for_viruses(file_bytes: bytes, filename: str) -> bool:
    result = await scan_file_with_clamav(file_bytes, filename)
    print(f"[file-service] Virus scan result: {result}", flush=True)
    return result.get("clean", False)

async def save_uploaded_file(
    upload,
    user_id: str,
    session: AsyncSession,
    is_chunked: bool = False,
    put_object_func=async_put_object
) -> FileRead:
    # Валидация имени файла
    filename = upload.filename
    # Защита от SQL-инъекций: запрещаем одинарную кавычку, точку с запятой, двойной дефис
    if (
        not filename
        or len(filename) > 255
        or re.search(r"[\\/:*?\"<>|']", filename)
        or ';' in filename
        or '--' in filename
    ):
        raise HTTPException(status_code=400, detail="Invalid file name")
    # Запрещённые расширения
    forbidden_exts = {'.exe', '.bat', '.cmd', '.sh'}
    ext = filename.lower().rsplit('.', 1)[-1] if '.' in filename else ''
    if ext and f'.{ext}' in forbidden_exts:
        raise HTTPException(status_code=415, detail="Forbidden file extension")
    # Проверка на дубликат
    dup_result = await session.execute(select(FileModel).where(FileModel.user_id == user_id, FileModel.filename == filename))
    duplicate = dup_result.scalar_one_or_none()
    if duplicate:
        raise HTTPException(status_code=409, detail="File with this name already exists")
    file_id = str(uuid.uuid4())
    storage_key = f"{user_id}/{file_id}/{filename}"
    max_size = 1 * 1024 * 1024
    total_size = 0
    chunk_size = 1024 * 1024  # 1 МБ
    # Стриминг: читаем файл по частям, сканируем и сразу отправляем в MinIO
    async def file_streamer() -> AsyncGenerator[bytes, None]:
        nonlocal total_size
        while True:
            chunk = await upload.read(chunk_size)
            if not chunk:
                break
            total_size += len(chunk)
            yield chunk

    # Проверка размера (если не chunked)
    # Для обычной загрузки ограничим 1 МБ, иначе chunked upload
    # Для MinIO нужен length заранее, поэтому считаем размер в процессе
    # Для вирус-сканирования — читаем файл в память, если размер позволяет
    # (или реализовать потоковое сканирование, если поддерживается)
    # Здесь реализуем вариант: если файл маленький — сканируем весь, если большой — отклоняем
    peek = await upload.read(chunk_size)
    if not is_chunked:
        if peek is None or len(peek) == 0:
            raise HTTPException(status_code=400, detail="Empty file is not allowed")
        if len(peek) > max_size:
            raise HTTPException(status_code=413, detail="File too large")
        if len(peek) > 15 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail=f"File too large for standard upload (> {CHUNK_MAX_SIZE // (1024*1024)}MB). Use chunked upload."
            )
    # Вирус-сканирование (только для файлов <= 1 МБ)
    is_clean = await scan_file_for_viruses(peek, filename)
    if not is_clean:
        raise HTTPException(status_code=400, detail="Файл заражён вирусом!")
    # После peek нужно вернуть указатель в начало
    await upload.seek(0)
    # Проверка content-type
    allowed_types = {"application/octet-stream", "text/plain"}
    if not upload.content_type or upload.content_type not in allowed_types:
        raise HTTPException(status_code=422, detail="Invalid content-type for upload")
    # Считаем размер и отправляем в MinIO
    content = await upload.read()
    total_size = len(content)
    # Финальная проверка размера
    if not is_chunked:
        if total_size == 0:
            raise HTTPException(status_code=400, detail="Empty file is not allowed")
        if total_size > max_size:
            raise HTTPException(status_code=413, detail="File too large")
        if total_size > 15 * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail=f"File too large for standard upload (> {CHUNK_MAX_SIZE // (1024*1024)}MB). Use chunked upload."
            )
    await upload.seek(0)
    await put_object_func(
        MINIO_BUCKET,
        storage_key,
        data=io.BytesIO(content),
        length=total_size,
        content_type=upload.content_type
    )
    db_file = FileModel(
        id=file_id,
        user_id=user_id,
        filename=filename,
        size=total_size,
        content_type=upload.content_type,
        storage_key=storage_key
    )
    session.add(db_file)
    await session.commit()
    # Обновление статистики пользователя
    await update_user_stat(user_id, "upload", len(content))
    return FileRead(
        id=db_file.id,
        user_id=db_file.user_id,
        filename=db_file.filename,
        size=db_file.size,
        content_type=db_file.content_type,
        created_at=db_file.created_at
    )


# ===== Chunked upload logic =====
CHUNKS_DIR = "/tmp/chunked_uploads" if os.name != "nt" else "tmp/chunked_uploads"
os.makedirs(CHUNKS_DIR, exist_ok=True)

CHUNK_MAX_SIZE = 15 * 1024 * 1024  # 15 МБ на чанк
META_DIR = os.path.join(CHUNKS_DIR, "meta")
os.makedirs(META_DIR, exist_ok=True)

def get_meta_path(upload_id):
    return os.path.join(META_DIR, f"{upload_id}.json")

async def save_file_chunk(chunk: UploadFile, chunk_number: int, total_chunks: int, upload_id: str, filename: str, user_id: str):
    meta_path = get_meta_path(upload_id)
    # Проверка content-type ДО любых операций
    allowed_types = {"application/octet-stream", "text/plain"}
    if not chunk.content_type or chunk.content_type not in allowed_types:
        raise HTTPException(status_code=422, detail="Invalid content-type for chunk upload")
    # Только если тип валиден — читаем чанк
    content = await chunk.read()
    if content is None or len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty chunk is not allowed")
    if len(content) > CHUNK_MAX_SIZE:
        raise HTTPException(status_code=413, detail=f"Chunk too large (>{CHUNK_MAX_SIZE // (1024*1024)}MB)")
    # Сохраняем чанк во временный файл
    chunk_dir = os.path.join(CHUNKS_DIR, upload_id)
    os.makedirs(chunk_dir, exist_ok=True)
    chunk_path = os.path.join(chunk_dir, f"chunk_{chunk_number:05d}")
    with open(chunk_path, "wb") as f:
        f.write(content)
    # Обновляем метаинформацию
    meta = {
        "upload_id": upload_id,
        "filename": filename,
        "user_id": user_id,
        "total_chunks": total_chunks,
        "received_chunks": [],
        "created_at": time.time()
    }
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    if chunk_number not in meta["received_chunks"]:
        meta["received_chunks"].append(chunk_number)
    meta["received_chunks"] = sorted(meta["received_chunks"])
    meta["updated_at"] = time.time()
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f)

async def assemble_chunks_if_complete(upload_id: str, filename: str, user_id: str, session: AsyncSession):
    meta_path = get_meta_path(upload_id)
    if not os.path.exists(meta_path):
        raise HTTPException(status_code=400, detail="No upload metadata found")
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    total_chunks = meta["total_chunks"]
    received_chunks = meta["received_chunks"]
    if len(received_chunks) != total_chunks:
        raise HTTPException(status_code=400, detail="Not all chunks uploaded yet")
    # Собираем все чанки в один файл
    chunk_dir = os.path.join(CHUNKS_DIR, upload_id)
    assembled_path = os.path.join(chunk_dir, filename)
    with open(assembled_path, "wb") as out_f:
        for i in range(1, total_chunks + 1):
            chunk_path = os.path.join(chunk_dir, f"chunk_{i:05d}")
            if not os.path.exists(chunk_path):
                raise HTTPException(status_code=400, detail=f"Missing chunk {i}")
            with open(chunk_path, "rb") as in_f:
                out_f.write(in_f.read())
    # Загружаем собранный файл в MinIO
    from minio_utils.minio_client import async_put_object, MINIO_BUCKET
    size = os.path.getsize(assembled_path)
    with open(assembled_path, "rb") as f:
        await async_put_object(MINIO_BUCKET, f"{user_id}/{upload_id}/{filename}", f, size, content_type="application/octet-stream")
    # Удаляем временные файлы
    for i in range(1, total_chunks + 1):
        chunk_path = os.path.join(chunk_dir, f"chunk_{i:05d}")
        if os.path.exists(chunk_path):
            os.remove(chunk_path)
    if os.path.exists(assembled_path):
        os.remove(assembled_path)
    if os.path.exists(meta_path):
        os.remove(meta_path)
    if os.path.exists(chunk_dir):
        try:
            os.rmdir(chunk_dir)
        except Exception:
            pass
    # Добавляем запись в БД
    db_file = FileModel(
        id=str(uuid.uuid4()),
        user_id=user_id,
        filename=filename,
        size=size,
        content_type="application/octet-stream",
        storage_key=f"{user_id}/{upload_id}/{filename}"
    )
    session.add(db_file)
    await session.commit()
    await update_user_stat(user_id, "upload", size)
    return FileRead(
        id=db_file.id,
        user_id=db_file.user_id,
        filename=db_file.filename,
        size=db_file.size,
        content_type=db_file.content_type,
        created_at=db_file.created_at
    )

# Очистка старых chunk'ов и метаданных (например, старше 4-х часов)
def cleanup_old_chunks(ttl_hours: int = 4):
    now = time.time()
    for meta_file in os.listdir(META_DIR):
        if not meta_file.endswith('.json'):
            continue
        meta_path = os.path.join(META_DIR, meta_file)
        try:
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
            updated_at = meta.get("updated_at", meta.get("created_at", now))
            if now - updated_at > ttl_hours * 3600:
                upload_id = meta["upload_id"]
                upload_dir = os.path.join(CHUNKS_DIR, upload_id)
                # Удаляем чанки
                if os.path.exists(upload_dir):
                    for fname in os.listdir(upload_dir):
                        os.remove(os.path.join(upload_dir, fname))
                    os.rmdir(upload_dir)
                os.remove(meta_path)
        except Exception as e:
            print(f"[cleanup] Failed to cleanup {meta_path}: {e}", flush=True)
