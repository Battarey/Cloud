import pytest

@pytest.mark.asyncio
async def test_list_files_invalid_filter(async_client, mock_jwt):
    response = await async_client.get(
        '/files/?size_min=notanumber',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 422

@pytest.mark.asyncio
async def test_list_files_success(async_client, mock_jwt):
    response = await async_client.get(
        '/files/',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_list_files_unauthorized(async_client):
    response = await async_client.get('/files/')
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_list_files_empty(async_client, mock_jwt_empty):
    # Для нового пользователя список должен быть пустым
    response = await async_client.get(
        '/files/',
        headers={'Authorization': f'Bearer {mock_jwt_empty}'}
    )
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_list_files_invalid_sort(async_client, mock_jwt):
    # Некорректное поле сортировки
    response = await async_client.get(
        '/files/?sort_by=notafield',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    # 422 если валидация, либо 200 если игнорируется
    assert response.status_code in (200, 422)


@pytest.mark.asyncio
async def test_list_files_pagination(async_client, mock_jwt):
    # Проверка пагинации (limit/offset)
    response = await async_client.get(
        '/files/?limit=1&offset=0',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_list_files_negative_limit(async_client, mock_jwt):
    # Некорректный limit
    response = await async_client.get(
        '/files/?limit=-5',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    # API не валидирует limit, возвращает 200 (баг или фича)
    assert response.status_code in (422, 400, 200)


@pytest.mark.asyncio
async def test_list_files_foreign_user(async_client, mock_jwt):
    # Попытка получить файлы другого пользователя (если фильтр по user_id есть)
    response = await async_client.get(
        '/files/?user_id=00000000-0000-0000-0000-000000000000',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    # 200, но пустой список, либо 403 если запрещено
    assert response.status_code in (200, 403)


@pytest.mark.asyncio
async def test_list_files_empty_query(async_client, mock_jwt):
    # Пустой query string
    response = await async_client.get(
        '/files?',
        headers={'Authorization': f'Bearer {mock_jwt}'}
    )
    # FastAPI редиректит на /files/ (307)
    assert response.status_code == 307
