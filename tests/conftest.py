import os
from typing import AsyncGenerator
from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import text
from src.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from src.database.database import engine, session_factory
from src.database.models import Base, Book
from src.main import app
from src.utils.enums import GenreEnum
from tests.test_auth import register_user

async def create_database():
    db_name = settings.POSTGRES_DB
    db_url = settings.DB_URL

    admin_url = db_url.replace(f"/{db_name}", "/postgres")
    admin_engine = create_async_engine(admin_url, isolation_level="AUTOCOMMIT")

    async with admin_engine.begin() as conn:
        await conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}"'))
        await conn.execute(text(f'CREATE DATABASE "{db_name}"'))

    await admin_engine.dispose()
    
# @pytest.fixture(scope='session', autouse=True)
# def event_loop():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     yield loop
#     loop.close()

@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    assert settings.MODE == "TEST"

    await create_database()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield
    await engine.dispose()

@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Fixture for an asynchronous FastAPI client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        try:
            yield ac
        finally:
            await ac.aclose()

@pytest.fixture(scope="session")
async def session():
    async with session_factory() as session:
        try:
            yield session
        finally:
            if session.in_transaction():
                await session.rollback()
            await session.close()

@pytest.fixture(scope="session")
async def test_books(register_user, session):
    author_id = register_user["user_id"] 

    books = [
        Book(title="Book 1", published_year=2020, genre=GenreEnum.BIOGRAPHY, author_id=author_id),
        Book(title="Book 2", published_year=2021, genre=GenreEnum.FANTASY, author_id=author_id),
    ]

    session.add_all(books)
    await session.commit()

    yield books

    for book in books:
        await session.delete(book)
            
    await session.commit()

@pytest.fixture(scope="session")
def test_files():
    base_path = os.path.join(os.path.dirname(__file__), 'content')
    return {
        'csv': ('test_book.csv', open(os.path.join(base_path, 'test_book.csv'), 'rb'), 'text/csv'),
        'csv_empty': ('test_empty_book.csv', open(os.path.join(base_path, 'test_empty_book.csv'), 'rb'), 'text/csv'),
        'json': ('test_book.json', open(os.path.join(base_path, 'test_book.json'), 'rb'), 'application/json'),
    }