from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from routers.book_router import router as book_router
from routers.auth_router import router as auth_router

# interface for entering a token (which is automatically sent to the headers) after login
http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/api/v1", dependencies=[Depends(http_bearer)])


router.include_router(book_router)
router.include_router(auth_router)
