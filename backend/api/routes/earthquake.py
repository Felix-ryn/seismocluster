from fastapi import APIRouter
from app.services.earthquake_service import get_earthquakes

router = APIRouter()

@router.get("/")
def earthquakes():
    return get_earthquakes()