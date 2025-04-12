from fastapi import status
from jwt import InvalidTokenError
from custom_exceptions.base_exceptions import AppException


class AuthException(AppException):
    """Base class for authentication errors"""
    pass

class UserCreateException(AuthException):
    def __init__(self, detail="Failed to create new user"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UserGetException(AuthException):
    def __init__(self, detail="Failed to get user by email"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UserUnexpectedError(AuthException):
    def __init__(self, detail="User create unexpected error"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthedUserException(AuthException):
    def __init__(self, detail="Invalid email or password"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class TokenNotFoundException(AuthException):
    def __init__(self, detail="Token invalid (user not found)"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class InvalidTokenErrorException(AuthException):
    def __init__(self, detail=f"Invalid token error: {InvalidTokenError}"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class InvalidTokenTypeException(AuthException):
    def __init__(self, detail="Invalid token type"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UserAlreadyExistsException(AuthException):
    def __init__(self, detail="User with this email already exists"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NotEnoughRightsException(AuthException):
    def __init__(self, detail="You have not enough rights"):
        super().__init__(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail=detail)
