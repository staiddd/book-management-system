from typing import List
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
from schemas.validation_schemas import BookFilterParams, BookSortParams


class BookRepository:
    def _build_conditions(self, filters: BookFilterParams) -> tuple:
        conditions = []
        params = {}

        if filters.book_id is not None:
            conditions.append("books.id = :book_id")
            params["book_id"] = filters.book_id

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
                SELECT books.id, books.title, books.published_year, books.genre, authors.id as author_id, authors.name as author_name
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
                    author=AuthorSchema(id=row.author_id, name=row.author_name)
                ) for row in books
            ]
        except Exception as e:
            raise BookGetException(str(e))
