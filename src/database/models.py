from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column, relationship
from typing import List
from utils.enums import GenreEnum


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class Author(Base):
    __tablename__ = "authors"
    
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    books: Mapped[List["Book"]] = relationship("Book", back_populates="author")

class Book(Base):
    __tablename__ = "books"
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    published_year: Mapped[int] = mapped_column(Integer, nullable=False)
    genre: Mapped[GenreEnum] = mapped_column(Enum(GenreEnum), nullable=False)
    
    author_id: Mapped[int] = mapped_column(ForeignKey("authors.id"), nullable=False)
    author: Mapped["Author"] = relationship("Author", back_populates="books")
