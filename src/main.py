from fastapi import FastAPI
from slowapi import Limiter, _rate_limit_exceeded_handler
from routers import router
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address
from config import settings


app = FastAPI(
    title="Book Management System API",
)

limiter = Limiter(key_func=get_remote_address, storage_uri=settings.REDIS_URL)
app.state.limiter = limiter

app.include_router(router)

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)