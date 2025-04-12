from typing import List, Optional
import uuid
from fastapi import Response, UploadFile
from constants import BOOK_FOLDER
from custom_exceptions.book_exceptions import BookDownloadException
from repositories.book_repository import BookRepository
from sqlalchemy.ext.asyncio import AsyncSession
from custom_exceptions.auth_exceptions import NotEnoughRightsException
from schemas.book_schemas import BookCreateSchema, BookNewSchema, BookSchema, BookUpdateSchema
from schemas.validation_schemas import BookFilterParams, BookSortParams
from utils.enums import GenreEnum
from aws.s3_actions import s3_client

class BookService:
    repository = BookRepository
    
    async def _check_book_author(
        self, session: AsyncSession, book_id: int, author_id: int
    ) -> None:
        """Checks that the user is the author of the book, otherwise throws an exception."""
        book: BookSchema = await self.repository.get_book_by_id(session, book_id)
        
        if book.author.id != author_id:
            raise NotEnoughRightsException()
    
    async def create_book(
        self, session: AsyncSession, title: str, 
        published_year: int, genre: GenreEnum, book_file: UploadFile, author_id: int
    ) -> BookNewSchema:
        file_path = f"{BOOK_FOLDER}/{uuid.uuid4()}_{book_file.filename}"
        book_insert = BookCreateSchema(title=title, published_year=published_year, genre=genre, file_path=file_path)
        # insert book file to s3 logic
        await s3_client.s3_upload_file(
            file=book_file,
            key=file_path,
        )

        return await self.repository.create_book(
            session=session,
            book_insert=book_insert,
            author_id=author_id
        )
    
    async def update_book(
        self, session: AsyncSession, title: Optional[str], 
        published_year: Optional[int], genre: Optional[GenreEnum], book_new_file: Optional[UploadFile], 
        author_id: int, book_id: int,
    ) -> BookNewSchema:
        await self._check_book_author(session, book_id, author_id)

        before_update_book = await self.get_book_by_id(session, book_id)

        file_path = f"{BOOK_FOLDER}/{uuid.uuid4()}_{book_new_file.filename}"
        book_update: BookUpdateSchema = BookUpdateSchema(title=title, published_year=published_year, genre=genre, file_path=file_path)

        book: BookNewSchema = await self.repository.update_book(
            session=session,
            book_update=book_update,
            book_id=book_id,
            author_id=author_id
        )
        # insert new book file (if hes not none) and delete existing file from s3 logic
        if book_new_file:
            await s3_client.s3_update_file(
                old_key=before_update_book.file_path,
                new_file=book_new_file,
                new_key=file_path
            )

        return book
    
    async def delete_book(
        self, session: AsyncSession, book_id: int, author_id: int
    ) -> None:
        await self._check_book_author(session, book_id, author_id)
        # delete existing file from s3 logic
        book = await self.repository.delete_book(
            session=session,
            book_id=book_id
        )
        await s3_client.s3_delete_file(book.file_path)

    
    async def get_book_by_id(
        self, session: AsyncSession, book_id: int,
    ) -> BookSchema:
        return await self.repository.get_book_by_id(
            session=session,
            book_id=book_id
        )

    async def get_books(
        self, session: AsyncSession, skip: int, limit: int, 
        filters: BookFilterParams, sorting: BookSortParams
    ) -> List[BookSchema]:
        return await self.repository.get_books(
            session=session, 
            skip=skip, 
            limit=limit,
            filters=filters,
            sorting=sorting,
        )
    
    async def download_book_file(
        self, file_name: str
    ) -> Response:
        try:
            contents = await s3_client.s3_download_file(
                key=f"{BOOK_FOLDER}/{file_name}",
            )
            return Response(
                content=contents,
                headers={
                    'Content-Disposition': f'attachment;filename={file_name}',
                    'Content-Type': 'application/octet-stream',
                }
            )
        except Exception as e:
            raise BookDownloadException(e)
