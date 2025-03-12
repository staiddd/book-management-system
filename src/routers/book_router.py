from fastapi import APIRouter

router = APIRouter(
    prefix="/book", 
    tags=["Book Operations"],
)