from fastapi import APIRouter
from app.services.summary_service import get_summary

router = APIRouter()

@router.get("/")
def summary():
    return get_summary()