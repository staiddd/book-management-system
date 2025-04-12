from fastapi import HTTPException
from auth.actions import create_access_token, create_refresh_token
from repositories.user_repository import UserRepository
from schemas.auth_schemas import TokenInfo, UserIn, UserOut
from sqlalchemy.ext.asyncio import AsyncSession
from custom_exceptions.auth_exceptions import UserAlreadyExistsException, UserUnexpectedError


class UserService:
    repository = UserRepository

    async def create_user(self, user_in: UserIn, session: AsyncSession):
        # Get user by email
        user: UserOut | None = await self.repository.get_user_by_email(
            session=session,
            email=user_in.email
        )

        # If the user exists raise HTTPException
        if user:
            raise UserAlreadyExistsException()
        try:
            # Create user using repository for user
            user_id = await self.repository.register_user(
                session=session,
                user_in=user_in
            )
            return {
                "user": {
                    "user_id": user_id,
                    **user_in.model_dump(exclude_defaults=True)
                    }
                }
        except HTTPException:
            raise
        except Exception as ex:
            raise UserUnexpectedError(f"Unexpected error: {ex}") 
        
    def login_user(self, user: UserOut):
        # Create access and refresh token using email
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        # Return access and refresh token
        return TokenInfo(
            access_token=access_token,
            refresh_token=refresh_token
        )
    
    def refresh_jwt(self, user: UserOut):
        access_token = create_access_token(user)
        return TokenInfo(
            access_token=access_token
        )