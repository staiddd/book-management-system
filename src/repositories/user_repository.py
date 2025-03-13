from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from auth.utils import hash_password
from schemas.auth_schemas import UserIn, UserOut

class UserRepository:
    async def register_user(
        self,
        session: AsyncSession, 
        user_in: UserIn,
    ) -> int:
        try:
            query = text("""
                INSERT INTO authors (name, email, password_hash)
                VALUES (:name, :email, :password_hash)
                RETURNING id;
            """)
            result = await session.execute(query, {
                "name": user_in.name,
                "email": user_in.email,
                "password_hash": hash_password(user_in.password_hash)
            })
            await session.commit()
            
            new_user_id = result.scalar_one()
            return new_user_id

        except Exception as ex:
            await session.rollback()
            return f"{ex}: failure to create new user"

    async def get_user_by_email(
        self,
        session: AsyncSession, 
        email: str,
    ) -> UserOut | None:
        query = text("""
            SELECT id, name, email, password_hash, created_at
            FROM authors 
            WHERE email = :email;
        """)
        result = await session.execute(query, {"email": email})
        user_row = result.fetchone()

        if user_row:
            return UserOut(
                id=user_row.id,
                name=user_row.name,
                email=user_row.email,
                password_hash=user_row.password_hash,
                created_at=user_row.created_at,
            )
        
        return None
    