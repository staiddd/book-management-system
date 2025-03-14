import csv
from io import StringIO
import json
from typing import List, Optional
from fastapi import APIRouter, Request, Response, UploadFile, status

from auth.validation import check_book_author
from constants import ALLOWED_FILE_TYPES, REQUIRED_FILE_FIELDS
from custom_exceptions.book_exceptions import BookBulkExportException, BookBulkImportException
from dependencies import (
    ValidateBatchSizeDep, FiltersDep,
    SessionDep, BookRepositoryDep, SortingDep, 
    UserDep, ValidateBookIdDep
)
from schemas.book_schemas import BookCreateSchema, BookNewSchema, BookSchema, BookUpdateSchema
from utils.enums import FileFormat, OnErrorEnum
from utils.util_funcs import parse_file, split_into_batches
from utils.validation_funcs import validate_book_data
from slowapi import Limiter
from slowapi.util import get_remote_address
from config import settings


router = APIRouter(
    prefix="/book", 
    tags=["Book Operations"],
)

limiter = Limiter(key_func=get_remote_address, storage_uri=settings.REDIS_URL)

@router.get('/', response_model=List[BookSchema])
@limiter.limit("5/minute")  # 5 requests in a minute
async def get_books(
    request: Request,
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

@router.get('/export/')
@limiter.limit("5/minute")  # 5 requests in a minute
async def export_books(
    request: Request,
    session: SessionDep,
    book_repo: BookRepositoryDep,
    filters: FiltersDep,
    sorting: SortingDep,
    skip: Optional[int] = 0,
    limit: Optional[int] = 10,
    format: Optional[FileFormat] = FileFormat.CSV
):
    books = await book_repo.get_books(
        session=session, 
        skip=skip, 
        limit=limit,
        filters=filters,
        sorting=sorting,
    )

    headers = [
        "ID", "Title", "Published Year", "Genre", "Author ID", "Author Name", "Created At", "Updated At"
    ]

    if format == FileFormat.CSV:
        output = StringIO()
        csv_writer = csv.writer(output)

        csv_writer.writerow(headers)

        for book in books:
            csv_writer.writerow([
                book.id,
                book.title,
                book.published_year,
                book.genre.value,
                book.author.id,
                book.author.name,
                book.created_at,
                book.updated_at
            ])

        output.seek(0)
        return Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=books_export.csv"}
        )

    elif format == FileFormat.JSON:
        books_data = [
            {
                "id": book.id,
                "title": book.title,
                "published_year": book.published_year,
                "genre": book.genre.value,
                "author_id": book.author.id,
                "author_name": book.author.name,
                "created_at": book.created_at.isoformat(),
                "updated_at": book.updated_at.isoformat()
            }
            for book in books
        ]

        return Response(
            content=json.dumps(books_data),
            media_type="application/json",
            headers={"Content-Disposition": "attachment; filename=books_export.json"}
        )

    else:
        raise BookBulkExportException()
    
@router.get('/{book_id}/', response_model=BookSchema)
@limiter.limit("5/minute")  # 5 requests in a minute
async def get_book_by_id(
    request: Request,
    session: SessionDep,
    book_repo: BookRepositoryDep,
    book_id: ValidateBookIdDep,
) -> BookSchema:
    return await book_repo.get_book_by_id(
        session=session,
        book_id=book_id
    )

@router.post('/', response_model=BookNewSchema, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # 5 requests in a minute
async def create_book(
    request: Request,
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
@limiter.limit("5/minute")  # 5 requests in a minute
async def bulk_import_books(
    request: Request,
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
@limiter.limit("5/minute")  # 5 requests in a minute
async def update_book(
    request: Request,
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
@limiter.limit("5/minute")  # 5 requests in a minute
async def delete_book(
    request: Request,
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

