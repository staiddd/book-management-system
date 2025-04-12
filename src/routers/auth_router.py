from typing import Annotated
from fastapi import APIRouter, Depends, Request, status

from auth.validation import validate_auth_user, get_current_auth_user_for_refresh
from dependencies import SessionDep, UserServiceDep
from schemas.auth_schemas import TokenInfo, UserIn, UserOut
from utils.limiter import limiter


router = APIRouter(
    prefix="/jwt/auth",
    tags=["Auth Operations"],
)

@router.post(
    "/signup/", 
    summary="Create new user",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("5/minute")  # 5 requests in a minute
async def create_user_handler(
    request: Request,
    session: SessionDep,
    user_in: UserIn,
    user_service: UserServiceDep,
):
    return await user_service.create_user(user_in, session)

@router.post(
    "/login/", 
    summary="Create access and refresh tokens for user", 
    response_model=TokenInfo
)
@limiter.limit("5/minute")  # 5 requests in a minute
async def login_handler(
    request: Request,
    user: Annotated[UserOut, Depends(validate_auth_user)],
    user_service: UserServiceDep,
) -> TokenInfo:
    return user_service.login_user(user)

@router.post(
    "/refresh/", 
    response_model=TokenInfo,
    response_model_exclude_none=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create new access token"
)
@limiter.limit("5/minute")  # 5 requests in a minute
async def auth_refresh_jwt(
    request: Request,
    user: Annotated[UserOut, Depends(get_current_auth_user_for_refresh)],
    user_service: UserServiceDep,
) -> TokenInfo:
    return user_service.refresh_jwt(user)