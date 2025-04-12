from typing import List, Optional
from fastapi import APIRouter, File, Form, Request, Response, UploadFile, status

from dependencies import (
    BookServiceDep,
    FiltersDep,
    SessionDep, SortingDep, 
    UserDep, ValidateBookIdDep
)
from schemas.book_schemas import BookNewSchema, BookSchema
from utils.limiter import limiter
from utils.enums import GenreEnum


router = APIRouter(
    prefix="/book", 
    tags=["Book Operations"],
)


@router.get('/', response_model=List[BookSchema])
@limiter.limit("5/minute")  # 5 requests in a minute
async def get_books(
    request: Request,
    session: SessionDep,
    book_service: BookServiceDep,
    filters: FiltersDep,
    sorting: SortingDep,
    skip: Optional[int] = 0,
    limit: Optional[int] = 10
) -> List[BookSchema]:
    return await book_service.get_books(
        session=session, 
        skip=skip, 
        limit=limit,
        filters=filters,
        sorting=sorting,
    )

@router.get("/download/", description="Enter only file name without folders")
@limiter.limit("5/minute")  # 5 requests in a minute
async def download_album_photo(
    request: Request,
    file_name: str,
    book_service: BookServiceDep,
) -> Response:
    return await book_service.download_book_file(
        file_name=file_name
    )
    
@router.get('/{book_id}/', response_model=BookSchema)
@limiter.limit("5/minute")  # 5 requests in a minute
async def get_book_by_id(
    request: Request,
    session: SessionDep,
    book_service: BookServiceDep,
    book_id: ValidateBookIdDep,
) -> BookSchema:
    return await book_service.get_book_by_id(
        session=session,
        book_id=book_id
    )

@router.post('/', response_model=BookNewSchema, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")  # 5 requests in a minute
async def create_book(
    request: Request,
    session: SessionDep,
    book_service: BookServiceDep,
    author: UserDep,
    title: str = Form(...),
    published_year: int = Form(gt=1800),
    genre: GenreEnum = Form(...),
    book_file: UploadFile = File(...)
) -> BookNewSchema:
    return await book_service.create_book(
        session=session,
        title=title,
        published_year=published_year,
        genre=genre,
        author_id=author.id,
        book_file=book_file
    )

@router.patch('/{book_id}/', response_model=BookNewSchema)
@limiter.limit("5/minute")  # 5 requests in a minute
async def update_book(
    request: Request,
    session: SessionDep,
    book_service: BookServiceDep,
    book_id: ValidateBookIdDep,
    author: UserDep,
    title: Optional[str] = Form(None),
    published_year: Optional[int] = Form(None, gt=1800),
    genre: Optional[GenreEnum] = Form(None),
    book_new_file: Optional[UploadFile] = File(None)
) -> BookNewSchema:
    return await book_service.update_book(
        session=session,
        book_id=book_id,
        author_id=author.id,
        title=title,
        published_year=published_year,
        genre=genre,
        book_new_file=book_new_file,
    )

@router.delete('/{book_id}/', status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("5/minute")  # 5 requests in a minute
async def delete_book(
    request: Request,
    session: SessionDep,
    book_service: BookServiceDep,
    book_id: ValidateBookIdDep,
    author: UserDep,
) -> None:
    return await book_service.delete_book(
        session=session,
        book_id=book_id,
        author_id=author.id,
    )

