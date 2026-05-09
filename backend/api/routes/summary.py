from fastapi import APIRouter
from app.services.summary_service import get_summary

router = APIRouter(
    prefix="/api/v1/summary",
    tags=["Summary"]
)

@router.get("/")
def summary():
    return get_summary()