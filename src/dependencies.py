from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import session_getter
from repositories.book_repository import BookRepository
from repositories.user_repository import UserRepository
from schemas.auth_schemas import UserOut
from schemas.validation_schemas import BookFilterParams, BookSortParams
from auth.validation import get_current_auth_user
from utils.util_funcs import get_filters, get_sorting
from utils.validation_funcs import validate_batch_size, validate_book_id


SessionDep = Annotated[AsyncSession, Depends(session_getter)]
BookRepositoryDep = Annotated[BookRepository, Depends(BookRepository)]
UserRepositoryDep = Annotated[UserRepository, Depends(UserRepository)]
FiltersDep = Annotated[BookFilterParams, Depends(get_filters)]
SortingDep = Annotated[BookSortParams, Depends(get_sorting)]
UserDep = Annotated[UserOut, Depends(get_current_auth_user)]
ValidateBatchSizeDep = Annotated[int, Depends(validate_batch_size)]
ValidateBookIdDep = Annotated[int, Depends(validate_book_id)]