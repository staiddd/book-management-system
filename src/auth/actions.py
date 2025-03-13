from datetime import timedelta
from schemas.auth_schemas import UserIn
from auth.utils import encode_jwt
from config import settings


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserIn) -> str:
    jwt_payload = {
        "sub": user.email,
        "name": user.name,
        "email": user.email,
        # "logged_in_at"
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.access_token_expire_minutes,
    )


def create_refresh_token(user: UserIn) -> str:
    jwt_payload = {
        "sub": user.email,
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.refresh_token_expire_days),
    )