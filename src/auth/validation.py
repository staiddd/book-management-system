from typing import Annotated
from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from auth.utils import (
    validate_password,
    decode_jwt
)
from constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, TOKEN_TYPE_FIELD
from database import session_getter
from repositories.book_repository import BookRepository
from repositories.user_repository import UserRepository
from schemas.auth_schemas import UserOut
from custom_exceptions.auth_exceptions import (
    unauthed_user_exception,
    invalid_token_type_exception,
    token_not_found_exception,
    invalid_token_error,
    not_enough_rights_exception
)
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.author_schemas import AuthorSchema
from schemas.book_schemas import BookSchema

# interface for entering name and password, and then automatically getting token and sending it in headers
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/jwt/auth/login/",
)

async def validate_auth_user(
    session: Annotated[AsyncSession, Depends(session_getter)],
    user_repo: Annotated[UserRepository, Depends(UserRepository)],
    email: str = Form(alias="username"),
    password: str = Form(),
):
    """Check that the user is registered"""
    # Get user by email
    if not (
        user := await user_repo.get_user_by_email(
            session=session, email=email
        )
    ):
        raise unauthed_user_exception

    if not validate_password(
        password=password,
        hashed_password=user.password_hash,
    ):
        raise unauthed_user_exception

    return user

async def validate_token_type(
    payload: dict, 
    token_type: str
) -> bool:
    """Checking the token type"""
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise invalid_token_type_exception


def get_current_token_payload(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> dict:
    """Getting information from a token"""
    try:
        payload = decode_jwt(
            token=token,
        )
    except InvalidTokenError:
        raise invalid_token_error
    return payload


async def get_user_by_token_sub(
    payload: dict,
    user_repo: UserRepository,
    session: AsyncSession
) -> UserOut:
    """Getting a user by the sub field from a token"""
    email: str | None = payload.get("sub")

    if email is None:
        raise token_not_found_exception

    user: UserOut | None = await user_repo.get_user_by_email(
        session=session, 
        email=email
    )
    
    if user:
        return user

    raise token_not_found_exception


# factory for creating functions (inputs the token type that is expected)
def get_auth_user_from_token_of_type(token_type: str):
    # Function to get information from a token
    async def get_auth_user_from_token(
        # we get the token from the headers
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_repo: Annotated[UserRepository, Depends(UserRepository)],
        session: Annotated[AsyncSession, Depends(session_getter)],
    ) -> UserOut:
        # check if the entered token matches the token in the header
        await validate_token_type(payload=payload, token_type=token_type)
        # we get data on the token
        return await get_user_by_token_sub(payload, user_repo, session)
    return get_auth_user_from_token


# Check that the user is authenticated to issue an access token
get_current_auth_user = get_auth_user_from_token_of_type(token_type=ACCESS_TOKEN_TYPE)
# Check that the user is authenticated to issue a refresh token
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(token_type=REFRESH_TOKEN_TYPE)

async def check_book_author(
    session: AsyncSession, 
    book_repo: BookRepository, 
    book_id: int, 
    author: AuthorSchema
) -> BookSchema:
    """Checks that the user is the author of the book, otherwise throws an exception."""
    book: BookSchema = await book_repo.get_book_by_id(session, book_id)
    
    if book.author.id != author.id:
        raise not_enough_rights_exception