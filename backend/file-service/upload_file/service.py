from sqlalchemy.ext.asyncio import AsyncSession
from models.file import File as FileModel
from schemas.file import FileRead
from minio_utils.minio_client import async_put_object, MINIO_BUCKET
from statistics.utils import update_user_stat
import uuid
from fastapi import HTTPException
import re
from sqlalchemy.future import select
import io
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
    content = await upload.read()
    # Ограничение размера файла (максимум 1 МБ для обычной загрузки, иначе советуем chunked upload)
    max_size = 1 * 1024 * 1024
    if len(content) > 15 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File too large for standard upload (> {CHUNK_MAX_SIZE // (1024*1024)}MB). Use chunked upload."
        )
    if not is_chunked and len(content) > max_size:
        raise HTTPException(status_code=413, detail="File too large")
    # Проверка на вирусы
    is_clean = await scan_file_for_viruses(content, filename)
    if not is_clean:
        raise HTTPException(status_code=400, detail="Файл заражён вирусом!")
    await put_object_func(
        MINIO_BUCKET,
        storage_key,
        data=io.BytesIO(content),
        length=len(content),
        content_type=upload.content_type
    )
    db_file = FileModel(
        id=file_id,
        user_id=user_id,
        filename=filename,
        size=len(content),
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
    upload_dir = os.path.join(CHUNKS_DIR, upload_id)
    os.makedirs(upload_dir, exist_ok=True)
    chunk_path = os.path.join(upload_dir, f"chunk_{chunk_number:05d}")
    content = await chunk.read()
    if len(content) > CHUNK_MAX_SIZE:
        raise HTTPException(status_code=413, detail=f"Chunk too large (>{CHUNK_MAX_SIZE // (1024*1024)}MB)")
    with open(chunk_path, "wb") as f:
        f.write(content)
    # Обновляем/создаём метаданные загрузки
    meta_path = get_meta_path(upload_id)
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
    upload_dir = os.path.join(CHUNKS_DIR, upload_id)
    meta_path = get_meta_path(upload_id)
    if not os.path.exists(meta_path):
        raise HTTPException(status_code=400, detail="No upload metadata found")
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    total_chunks = meta["total_chunks"]
    received_chunks = meta["received_chunks"]
    if len(received_chunks) != total_chunks:
        raise HTTPException(status_code=400, detail="Not all chunks uploaded")
    chunk_files = [f"chunk_{i:05d}" for i in received_chunks]
    assembled_path = os.path.join(upload_dir, filename)
    with open(assembled_path, "wb") as out_f:
        for chunk_file in chunk_files:
            with open(os.path.join(upload_dir, chunk_file), "rb") as in_f:
                out_f.write(in_f.read())
    class AssembledUpload:
        def __init__(self, path, filename):
            self.filename = filename
            self.content_type = "application/octet-stream"
            self._path = path
        async def read(self):
            with open(self._path, "rb") as f:
                return f.read()
    assembled_upload = AssembledUpload(assembled_path, filename)
    result = await save_uploaded_file(assembled_upload, user_id, session, is_chunked=True)
    # После успешной сборки — удаляем временные файлы и метаданные
    for f in chunk_files:
        os.remove(os.path.join(upload_dir, f))
    os.remove(assembled_path)
    os.remove(meta_path)
    os.rmdir(upload_dir)
    return result

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
