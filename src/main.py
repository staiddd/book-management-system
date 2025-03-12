from fastapi import FastAPI
from routers import router


app = FastAPI(
    title="Book Management System API",
)

app.include_router(router)