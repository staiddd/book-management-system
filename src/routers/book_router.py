from typing import Annotated, List, Optional
from fastapi import APIRouter, Depends, UploadFile, status

from custom_exceptions.book_exceptions import BookBulkImportException
from dependencies import FiltersDep, SessionDep, BookRepositoryDep, SortingDep
from schemas.auth_schemas import UserOut
from schemas.book_schemas import BookCreateSchema, BookNewSchema, BookSchema, BookUpdateSchema
from utils.enums import OnErrorEnum
from utils.util_funcs import parse_file, split_into_batches
from utils.validation_funcs import validate_batch_size, validate_book_data, validate_book_id


router = APIRouter(
    prefix="/book", 
    tags=["Book Operations"],
)

@router.get('/', response_model=List[BookSchema])
async def get_books(
    session: SessionDep,
    book_repo: BookRepositoryDep,
    filters: FiltersDep,
    sorting: SortingDep,
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

@router.post('/', response_model=BookNewSchema, status_code=status.HTTP_201_CREATED)
async def create_book(
    session: SessionDep,
    book_repo: BookRepositoryDep,
    book_insert: BookCreateSchema,
    author: Annotated[UserOut, Depends(get_current_auth_user)],
) -> BookNewSchema:
    return await book_repo.create_book(
        session=session,
        book_insert=book_insert
    )

@router.post('/import/', status_code=status.HTTP_201_CREATED)
async def bulk_import_books(
    session: SessionDep,
    book_repo: BookRepositoryDep,
    file: UploadFile,
    on_validation_error: OnErrorEnum = OnErrorEnum.RAISE_ERROR,
    batch_size: int = Depends(validate_batch_size),
):
    try:
        data = await parse_file(file)

        for batch in split_into_batches(data, batch_size):
            validated_data: list[BookCreateSchema] = validate_book_data(batch, on_validation_error)

            if not validated_data:
                return {"message": "empty"}
            
            await book_repo.create_books_bulk(session, validated_data)

        return {"message": "success"}

    except Exception as e:
        await session.rollback()
        raise BookBulkImportException(f"Unexptected error while bulk importing books: {str(e)}")


@router.patch('/{book_id}/', response_model=BookNewSchema)
async def update_book(
    session: SessionDep,
    book_repo: BookRepositoryDep,
    book_update: BookUpdateSchema,
    book_id: int = Depends(validate_book_id),
) -> BookNewSchema:
    return await book_repo.update_book(
        session=session,
        book_update=book_update,
        book_id=book_id,
    )

@router.delete('/{book_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    session: SessionDep,
    book_repo: BookRepositoryDep,
    book_id: int = Depends(validate_book_id),
) -> None:
    return await book_repo.delete_book(
        session=session,
        book_id=book_id
    )

