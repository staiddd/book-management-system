from fastapi import APIRouter
from routers.book_router import router as book_router


router = APIRouter(prefix="/api/v1")


router.include_router(book_router)
