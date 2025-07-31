import pytest
from minio import Minio
from cryptography.fernet import Fernet
import os
import jwt

@pytest.mark.asyncio
async def test_full_crypto_flow(async_client, mock_jwt_empty, get_user_key_from_db):
    """
    Полный цикл: upload -> проверка в MinIO -> download -> direct link
    """
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    file_content = b"super secret data"
    filename = "crypto_test.txt"
    # 1. Upload
    resp = await async_client.post(
        '/files/upload',
        files={'upload': (filename, file_content, 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert resp.status_code == 200
    file_id = resp.json()["id"]
    storage_key = resp.json().get("storage_key") or f"{user_id}/{file_id}/{filename}"

    # 2. Проверка файла в MinIO (он должен быть зашифрован)
    minio_client = Minio(
        os.getenv("MINIO_ENDPOINT", "minio:9000"),
        access_key=os.getenv("MINIO_ACCESS_KEY", "minioadmin"),
        secret_key=os.getenv("MINIO_SECRET_KEY", "minioadmin"),
        secure=False
    )
    obj = minio_client.get_object(os.getenv("MINIO_BUCKET", "files"), storage_key)
    encrypted_data = obj.read()
    assert encrypted_data != file_content

    # 3. Получение ключа пользователя
    user_key = get_user_key_from_db(user_id)
    decrypted = Fernet(user_key).decrypt(encrypted_data)
    assert decrypted == file_content

    # 4. Download через API (файл должен быть расшифрован)
    download_resp = await async_client.get(f"/files/{file_id}", headers={"Authorization": f"Bearer {mock_jwt_empty}"})
    assert download_resp.status_code == 200
    assert download_resp.content == file_content

    # 5. Direct download link
    direct_resp = await async_client.get(f"/generate-link/direct/{file_id}/{user_id}")
    assert direct_resp.status_code == 200
    assert direct_resp.content == file_content

@pytest.mark.asyncio
async def test_crypto_resilience_missing_key(async_client, mock_jwt_empty, remove_user_key_from_db):
    """
    Проверка: если ключ пользователя удалён, скачивание невозможно
    """
    user_id = jwt.decode(mock_jwt_empty, options={"verify_signature": False})["sub"]
    file_content = b"fail test"
    filename = "fail.txt"
    resp = await async_client.post(
        '/files/upload',
        files={'upload': (filename, file_content, 'text/plain')},
        headers={'Authorization': f'Bearer {mock_jwt_empty}'},
        params={'user_id': user_id}
    )
    assert resp.status_code == 200
    file_id = resp.json()["id"]
    # Удаляем ключ пользователя
    remove_user_key_from_db(user_id)
    # Попытка скачать
    download_resp = await async_client.get(f"/files/{file_id}", headers={"Authorization": f"Bearer {mock_jwt_empty}"})
    assert download_resp.status_code in (404, 500)
    # Попытка скачать по ссылке
    direct_resp = await async_client.get(f"/generate-link/direct/{file_id}/{user_id}")
    assert direct_resp.status_code in (404, 500)

# Фикстуры get_user_key_from_db и remove_user_key_from_db должны быть реализованы в conftest.py или здесь
# Они должны работать с вашей БД user_keys
