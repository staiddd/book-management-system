from typing import List
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.book_schemas import BookCreateSchema, BookNewSchema, BookSchema
from schemas.author_schemas import AuthorSchema

from custom_exceptions.book_exceptions import (
    BookCreateException,
    BookDeleteException,
    BookGetException,
    BookNotFoundException,
    BookUpdateException,
)
from schemas.validation_schemas import BookFilterParams, BookSortParams


class BookRepository:
    def _build_conditions(self, filters: BookFilterParams) -> tuple:
        conditions = []
        params = {}

        if filters.title:
            conditions.append("books.title ILIKE :title")
            params["title"] = f"%{filters.title}%"

        if filters.year is not None:
            conditions.append("books.published_year = :year")
            params["year"] = filters.year

        if filters.author_name:
            conditions.append("authors.name ILIKE :author_name")
            params["author_name"] = f"%{filters.author_name}%"

        return " AND ".join(conditions) if conditions else "1=1", params

    async def get_books(
        self,
        session: AsyncSession,
        filters: BookFilterParams,
        sorting: BookSortParams,
        skip: int = 0,
        limit: int = 10,
    ) -> List[BookSchema]:
        try:
            order_clause = f"books.{sorting.order_by} {'DESC' if sorting.order_desc else 'ASC'}"
            
            where_clause, params = self._build_conditions(filters)
            params.update({
                "skip": skip,
                "limit": limit,
            })
            
            query = f"""
                 SELECT 
                    books.id, books.title, books.published_year, books.genre, books.created_at, books.updated_at,
                    authors.id as author_id, authors.name as author_name, authors.created_at as author_created_at
                FROM books
                JOIN authors ON books.author_id = authors.id
                WHERE {where_clause}
                ORDER BY {order_clause}
                OFFSET :skip LIMIT :limit
            """
            
            result = await session.execute(text(query), params)
            books = result.fetchall()
            
            return [
                BookSchema(
                    id=row.id,
                    title=row.title,
                    published_year=row.published_year,
                    genre=row.genre,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                    author=AuthorSchema(id=row.author_id, name=row.author_name, created_at=row.author_created_at)
                ) for row in books
            ]
        except Exception as e:
            raise BookGetException(str(e))
        
    async def get_book_by_id(
        self,
        session: AsyncSession,
        book_id: int,
    ) -> BookSchema:
        try:
            query = """
                SELECT 
                    books.id, books.title, books.published_year, books.genre, books.created_at, books.updated_at, 
                    authors.id as author_id, authors.name as author_name, authors.created_at as author_created_at
                FROM books
                JOIN authors ON books.author_id = authors.id
                WHERE books.id = :book_id
                LIMIT 1
            """
            
            params = {"book_id": book_id}
            
            result = await session.execute(text(query), params)
            book = result.fetchone()

            if not book:
                raise BookNotFoundException()

            return BookSchema(
                id=book.id,
                title=book.title,
                published_year=book.published_year,
                genre=book.genre,
                created_at=book.created_at,
                updated_at=book.updated_at,
                author=AuthorSchema(id=book.author_id, name=book.author_name, created_at=book.author_created_at)
            )
        
        except Exception as e:
            raise BookGetException(str(e))

    async def create_book(
        self,
        session: AsyncSession,
        book_insert: BookCreateSchema
    ) -> BookNewSchema:
        try:
            query = """
                INSERT INTO books (title, published_year, genre, author_id)
                VALUES (:title, :published_year, :genre, :author_id)
                RETURNING id, title, published_year, genre, author_id, created_at, updated_at;
            """
            
            params = {
                "title": book_insert.title,
                "published_year": book_insert.published_year,
                "genre": book_insert.genre.value.upper(),
                "author_id": book_insert.author_id
            }

            result = await session.execute(text(query), params)
            new_book = result.fetchone()

            await session.commit()

            if not new_book:
                raise BookCreateException("Failed to create book")

            return BookNewSchema(
                id=new_book.id,
                title=new_book.title,
                published_year=new_book.published_year,
                genre=new_book.genre,
                author_id=new_book.author_id,
                created_at=new_book.created_at,
                updated_at=new_book.updated_at
            )

        except Exception as e:
            await session.rollback()
            raise BookCreateException(f"Error while creating book: {str(e)}")