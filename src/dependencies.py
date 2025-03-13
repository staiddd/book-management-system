from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import session_getter
from repositories.book_repository import BookRepository


SessionDep = Annotated[AsyncSession, Depends(session_getter)]
BookRepositoryDep = Annotated[BookRepository, Depends(BookRepository)]