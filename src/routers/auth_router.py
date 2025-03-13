from typing import Annotated
from fastapi import APIRouter, Depends, status

from auth.actions import create_access_token, create_refresh_token
from auth.validation import validate_auth_user, get_current_auth_user_for_refresh
from dependencies import SessionDep, UserRepositoryDep
from schemas.auth_schemas import TokenInfo, UserIn, UserOut
from custom_exceptions.auth_exceptions import user_already_exists_exception


router = APIRouter(
    prefix="/jwt/auth",
    tags=["Auth Operations"],
)


@router.post(
    "/signup/", 
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
)
async def create_user_handler(
    session: SessionDep,
    user_repo: UserRepositoryDep,
    user_in: UserIn
):
    # Get user by email
    user: UserOut | None = await user_repo.get_user_by_email(
        session=session,
        email=user_in.email
    )

    # If the user exists raise HTTPException
    if user:
        raise user_already_exists_exception
    try:
        # Create user using repository for user
        user_id = await user_repo.register_user(
            session=session,
            user_in=user_in
        )
        return {
            "user": {
                "user_id": user_id,
                **user_in.model_dump(exclude_defaults=True)
                }
            }
    except Exception as ex:
        return f"{ex}: failure to create new user"

@router.post(
    "/login/", 
    summary="Create access and refresh tokens for user", 
    response_model=TokenInfo
)
async def login_handler(
    user: Annotated[UserOut, Depends(validate_auth_user)],
) -> TokenInfo:
    # Create access and refresh token using email
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    # Return access and refresh token
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post(
    "/refresh/", 
    response_model=TokenInfo,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create new access token"
)
async def auth_refresh_jwt(
    user: Annotated[UserOut, Depends(get_current_auth_user_for_refresh)],
) -> TokenInfo: 
    access_token = create_access_token(user)
    return TokenInfo(
        access_token=access_token
    )