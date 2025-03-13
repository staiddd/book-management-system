from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import session_getter
from repositories.book_repository import BookRepository
from repositories.user_repository import UserRepository
from schemas.validation_schemas import BookFilterParams, BookSortParams
from utils.util_funcs import get_filters, get_sorting


SessionDep = Annotated[AsyncSession, Depends(session_getter)]
BookRepositoryDep = Annotated[BookRepository, Depends(BookRepository)]
UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]
FiltersDep = Annotated[BookFilterParams, Depends(get_filters)]
SortingDep = Annotated[BookSortParams, Depends(get_sorting)]