from typing import List, Optional
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.book_schemas import BookSchema
from schemas.author_schemas import AuthorSchema

from custom_exceptions.book_exceptions import (
    BookCreateException,
    BookDeleteException,
    BookGetException,
    BookUpdateException,
)


class BookRepository:
    async def get_books(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 10,
        book_id: Optional[int] = None,
        title: Optional[str] = None,
        year: Optional[int] = None,
        author_name: Optional[str] = None,
        order_by: Optional[str] = "id",
        order_desc: bool = False,
    ) -> List[BookSchema]:
        try:
            order_clause = f"books.{order_by} {'DESC' if order_desc else 'ASC'}"
            query = f"""
                SELECT books.id, books.title, books.published_year, books.genre, authors.id as author_id, authors.name as author_name
                FROM books
                JOIN authors ON books.author_id = authors.id
                WHERE (:book_id IS NULL OR books.id = :book_id)
                AND (:title IS NULL OR books.title ILIKE :title)
                AND (:year IS NULL OR books.published_year = :year)
                AND (:author_name IS NULL OR authors.name ILIKE :author_name)
                ORDER BY {order_clause}
                OFFSET :skip LIMIT :limit
            """
            
            params = {
                "book_id": book_id,
                "title": f"%{title}%" if title else None,
                "year": year,
                "author_name": f"%{author_name}%" if author_name else None,
                "skip": skip,
                "limit": limit,
            }
            
            result = await session.execute(text(query), params)
            books = result.fetchall()
            
            return [
                BookSchema(
                    id=row.id,
                    title=row.title,
                    published_year=row.published_year,
                    genre=row.genre,
                    author=AuthorSchema(id=row.author_id, name=row.author_name)
                ) for row in books
            ]
        except Exception as e:
            raise BookCreateException(str(e))