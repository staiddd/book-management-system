from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Author
from auth.utils import hash_password
from schemas.auth_schemas import UserIn, UserOut
from custom_exceptions.auth_exceptions import UserCreateException, UserGetException


class UserRepository:
    @classmethod
    async def register_user(
        cls,
        session: AsyncSession, 
        user_in: UserIn,
    ) -> int:
        try:
            new_user: Author = Author(
                name=user_in.name,
                email=user_in.email,
                password_hash=hash_password(user_in.password_hash)
            )
            session.add(new_user)
            await session.commit()
            return new_user.id
        except Exception as e:
            await session.rollback()
            raise UserCreateException(f"Failed to create new user: {e}")

    @classmethod
    async def get_user_by_email(
        cls,
        session: AsyncSession, 
        email: str,
    ) -> UserOut | None:
        try:
            stmt = (
                select(Author)
                .where(Author.email==email)
            )
            result = await session.scalars(stmt)
            user: Author | None = result.one_or_none()

            if user:
                return UserOut(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    password_hash=user.password_hash,
                    created_at=user.created_at,
                )
            
            return None
        except Exception as e:
            raise UserGetException(f"Failed to get user by email: {e}")
    