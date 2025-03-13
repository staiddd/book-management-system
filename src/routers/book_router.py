from typing import List, Optional
from fastapi import APIRouter, Depends

from dependencies import SessionDep, BookRepositoryDep
from schemas.book_schemas import BookSchema
from schemas.validation_schemas import BookFilterParams, BookSortParams
from utils.util_funcs import get_filters, get_sorting


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