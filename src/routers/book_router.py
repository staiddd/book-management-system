from typing import List, Optional
from fastapi import APIRouter, Depends

from dependencies import SessionDep, BookRepositoryDep
from schemas.book_schemas import BookSchema
from schemas.validation_schemas import BookFilterParams, BookSortParams
from utils.util_funcs import get_filters, get_sorting
from utils.validation_funcs import validate_book_id


router = APIRouter(
    prefix="/book", 
    tags=["Book Operations"],
)

@router.get('/', response_model=List[BookSchema])
async def get_books(
    session: SessionDep,
    book_repo: BookRepositoryDep,
    filters: BookFilterParams = Depends(get_filters),
    sorting: BookSortParams = Depends(get_sorting),
    skip: Optional[int] = 0,
    limit: Optional[int] = 10
) -> List[BookSchema]:
    return await book_repo.get_books(
        session=session, 
        skip=skip, 
        limit=limit,
        filters=filters,
        sorting=sorting,
    )

@router.get('/{book_id}/', response_model=BookSchema)
async def get_book_by_id(
    session: SessionDep,
    book_repo: BookRepositoryDep,
    book_id: int = Depends(validate_book_id),
) -> BookSchema:
    return await book_repo.get_book_by_id(
        session=session,
        book_id=book_id
    )
