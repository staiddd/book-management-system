from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine, 
    AsyncEngine, async_sessionmaker, AsyncSession)
from config import settings



# Create an asynchronous engine for the database connection
engine: AsyncEngine = create_async_engine(
    url=settings.DATABASE_URL,
    echo=False,
    echo_pool=False,
    pool_size=5,
    max_overflow=5,
)


# Create a session factory for generating asynchronous sessions
session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    autoflush=False,
    class_=AsyncSession,
    autocommit=False,
    expire_on_commit=False
)

async def session_getter() -> AsyncGenerator[AsyncSession, None]:
    """
        Asynchronous generator function that provides
        a session from the session factory.
    """
    async with session_factory() as session:
        try:
            yield session
        finally:
            if session.in_transaction():
                await session.rollback()
            await session.close()
