from typing import List, Optional
from fastapi import APIRouter, UploadFile, status

from auth.validation import check_book_author
from constants import ALLOWED_FILE_TYPES, REQUIRED_FILE_FIELDS
from custom_exceptions.book_exceptions import BookBulkImportException
from dependencies import (
    ValidateBatchSizeDep, FiltersDep,
    SessionDep, BookRepositoryDep, SortingDep, 
    UserDep, ValidateBookIdDep
)
from schemas.book_schemas import BookCreateSchema, BookNewSchema, BookSchema, BookUpdateSchema
from utils.enums import OnErrorEnum
from utils.util_funcs import parse_file, split_into_batches
from utils.validation_funcs import validate_book_data


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
    book_id: ValidateBookIdDep,
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
    author: UserDep,
) -> BookNewSchema:
    return await book_repo.create_book(
        session=session,
        book_insert=book_insert,
        author_id=author.id
    )

@router.post(
    '/import/', 
    status_code=status.HTTP_201_CREATED, 
    description=f'Required fields: {", ".join(REQUIRED_FILE_FIELDS)}. Allowed file types: {", ".join(ALLOWED_FILE_TYPES)}'
)
async def bulk_import_books(
    session: SessionDep,
    book_repo: BookRepositoryDep,
    file: UploadFile,
    author: UserDep,
    batch_size: ValidateBatchSizeDep,
    on_validation_error: OnErrorEnum = OnErrorEnum.RAISE_ERROR,
):
    try:
        data = await parse_file(file)

        if not data:
            return {"message": "empty"}

        for batch in split_into_batches(data, batch_size):
            validated_data: list[dict] = validate_book_data(batch, on_validation_error)          
            await book_repo.create_books_bulk(session, validated_data, author.id)

        return {"message": "success"}

    except Exception as e:
        await session.rollback()
        raise BookBulkImportException(f"Unexptected error while bulk importing books: {str(e)}")


@router.patch('/{book_id}/', response_model=BookNewSchema)
async def update_book(
    session: SessionDep,
    book_repo: BookRepositoryDep,
    book_update: BookUpdateSchema,
    book_id: ValidateBookIdDep,
    author: UserDep,
) -> BookNewSchema:
    await check_book_author(session, book_repo, book_id, author)

    return await book_repo.update_book(
        session=session,
        book_update=book_update,
        book_id=book_id,
        author_id=author.id
    )

@router.delete('/{book_id}/', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    session: SessionDep,
    book_repo: BookRepositoryDep,
    book_id: ValidateBookIdDep,
    author: UserDep,
) -> None:
    await check_book_author(session, book_repo, book_id, author)

    return await book_repo.delete_book(
        session=session,
        book_id=book_id
    )

