from httpx import AsyncClient
import pytest
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.book_schemas import BookSchema, BookNewSchema
from src.repositories.book_repository import BookRepository
from src.schemas.validation_schemas import BookFilterParams, BookSortParams
from tests.test_auth import login_user

API_URL = "api/v1/book/"

async def validate_pydantic_schema(data, schema):
    try:
        return schema.model_validate(data)
    except ValidationError as e:
        pytest.fail(f"Pydantic validation error: {e}")

@pytest.mark.asyncio(loop_scope="session")
async def test_get_books(ac: AsyncClient, test_books: list):
    response = await ac.get(API_URL)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(test_books)
    [await validate_pydantic_schema(book, BookSchema) for book in data]

@pytest.mark.asyncio(loop_scope="session")
async def test_get_book_by_id(ac: AsyncClient, test_books: list):
    book_id = test_books[0].id
    response = await ac.get(f"{API_URL}{book_id}/")
    assert response.status_code == 200
    data = response.json()
    validated_book = await validate_pydantic_schema(data, BookSchema)
    assert validated_book.id == book_id

@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("auth", [True, False])
async def test_create_book(ac: AsyncClient, login_user, session: AsyncSession, auth):
    headers = {"Authorization": f"Bearer {login_user['access_token']}"} if auth else {}
    payload = {"title": "Test Book", "published_year": 2021, "genre": "FICTION"}
    
    response = await ac.post(API_URL, json=payload, headers=headers)
    if auth:
        assert response.status_code == 201
        await validate_pydantic_schema(response.json(), BookNewSchema)
        all_books = await BookRepository().get_books(session, sorting=BookSortParams(), filters=BookFilterParams())
        assert any(book.title == payload["title"] for book in all_books)
    else:
        assert response.status_code == 401

@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("auth", [True, False])
async def test_update_book(ac: AsyncClient, test_books: list, login_user, session: AsyncSession, auth):
    book_id = test_books[0].id
    headers = {"Authorization": f"Bearer {login_user['access_token']}"} if auth else {}
    payload = {"title": "Updated Title", "published_year": 2022, "genre": "FICTION"}
    
    response = await ac.patch(f"{API_URL}{book_id}/", json=payload, headers=headers)
    if auth:
        assert response.status_code == 200
        updated_book = await BookRepository().get_book_by_id(session, book_id)
        assert updated_book.title == payload["title"]
    else:
        assert response.status_code == 401

@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("auth", [True, False])
async def test_delete_book(ac: AsyncClient, test_books: list, login_user, session: AsyncSession, auth):
    book_id = test_books[0].id
    headers = {"Authorization": f"Bearer {login_user['access_token']}"} if auth else {}

    response = await ac.delete(f"{API_URL}{book_id}/", headers=headers)
    if auth:
        assert response.status_code == 204
        all_books = await BookRepository().get_books(session, sorting=BookSortParams(), filters=BookFilterParams())
        assert not any(book.id == book_id for book in all_books)
    else:
        assert response.status_code == 401

@pytest.mark.asyncio(loop_scope="session")
@pytest.mark.parametrize("auth, batch_size, file_type, expected_message", [
    (True, 1, 'csv', "success"),
    (True, 100, 'json', "success"),
    (True, 100, 'csv_empty', "empty"),
    (False, 1, 'csv', "empty"),
])
async def test_import_books_from_file(ac: AsyncClient, login_user, test_files, auth, batch_size, file_type, expected_message):
    headers = {"Authorization": f"Bearer {login_user['access_token']}"} if auth else {}
    file = test_files[file_type]

    response = await ac.post(f"{API_URL}import/", files={"file": file}, headers=headers, params={"batch_size": batch_size})
    
    if auth:
        assert response.status_code == 201
        data = response.json()
        assert "message" in data
        assert data["message"] == expected_message
    else:
        assert response.status_code == 401
