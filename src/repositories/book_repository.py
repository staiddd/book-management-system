from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Author, Book
from schemas.book_schemas import BookCreateSchema, BookNewSchema, BookSchema, BookUpdateSchema
from sqlalchemy.orm import joinedload
from custom_exceptions.book_exceptions import (
    BookCreateException,
    BookDeleteException,
    BookGetException,
    BookNotFoundException,
    BookUpdateException,
)
from schemas.validation_schemas import BookFilterParams, BookSortParams


class BookRepository:
    @classmethod
    async def get_books(
        cls,
        session: AsyncSession,
        filters: BookFilterParams,
        sorting: BookSortParams,
        skip: int = 0,
        limit: int = 10,
    ) -> List[BookSchema]:
        try:
            query = select(Book).options(joinedload(Book.author))
            
            if filters.title:
                query = query.filter(Book.title.ilike(f"%{filters.title}%"))
            if filters.published_year is not None:
                query = query.filter(Book.published_year == filters.published_year)
            if filters.author_name:
                query = query.join(Author).filter(Author.name.ilike(f"%{filters.author_name}%"))
            
            if sorting.order_by:
                order_column = getattr(Book, sorting.order_by, None)
                if order_column:
                    query = query.order_by(order_column.desc() if sorting.order_desc else order_column.asc())
            
            query = query.offset(skip).limit(limit)
            
            result = await session.execute(query)
            return [book for book in result.scalars().all()]
        except Exception as e:
            raise BookGetException(str(e))
    
    @classmethod
    async def get_book_by_id(
        cls, session: AsyncSession, book_id: int
    ) -> BookSchema:
        try:
            query = select(Book).options(joinedload(Book.author)).filter(Book.id == book_id)
            result = await session.execute(query)
            book = result.scalar_one_or_none()
            if not book:
                raise BookNotFoundException()
            return book
        except Exception as e:
            raise BookGetException(str(e))
    
    @classmethod
    async def create_book(
        cls, session: AsyncSession, book_insert: BookCreateSchema, author_id: int
    ) -> BookNewSchema:
        try:
            new_book = Book(
                title=book_insert.title,
                published_year=book_insert.published_year,
                genre=book_insert.genre.value,
                author_id=author_id,
                file_path=book_insert.file_path
            )
            session.add(new_book)
            await session.commit()
            await session.refresh(new_book)
            return new_book
        except Exception as e:
            await session.rollback()
            raise BookCreateException(f"Error while creating book: {str(e)}")
    
    @classmethod
    async def update_book(
        cls, session: AsyncSession, book_update: BookUpdateSchema, book_id: int, author_id: int
    ) -> BookNewSchema:
        try:
            query = select(Book).filter(Book.id == book_id)
            result = await session.execute(query)
            book = result.scalar_one_or_none()
            if not book:
                raise BookNotFoundException()
            
            if book_update.title:
                book.title = book_update.title
            if book_update.published_year is not None:
                book.published_year = book_update.published_year
            if book_update.genre:
                book.genre = book_update.genre.value
            if book_update.file_path:
                book.file_path = book_update.file_path
            book.author_id = author_id
            
            await session.commit()
            await session.refresh(book)
            return book
        except Exception as e:
            await session.rollback()
            raise BookUpdateException(f"Error while updating book: {str(e)}")

    @classmethod
    async def delete_book(
        cls,
        session: AsyncSession,
        book_id: int
    ) -> Book:
        try:
            book = await session.get(Book, book_id)
            await session.delete(book)
            await session.commit()
            return book
        except Exception as e:
            await session.rollback()
            raise BookDeleteException(f"Error while deleting book: {str(e)}")
