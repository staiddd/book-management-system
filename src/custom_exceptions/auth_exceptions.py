from fastapi import HTTPException, status
from jwt import InvalidTokenError


unauthed_user_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="invalid email or password",
)


token_not_found_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="token invalid (user not found)",
)


invalid_token_error = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"invalid token error: {InvalidTokenError}",
)


invalid_token_type_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"invalid token type"
)


user_already_exists_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="User with this email already exists"
)


user_not_found_exception = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User not found"
)


update_ban_status_exception = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Failed to update user's ban status"
)

not_enough_rights_exception = HTTPException(
    status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
    detail=f"You have not enough rights"
)