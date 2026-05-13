from fastapi import APIRouter, Query, HTTPException

from app.schemas.earthquake_schema import EarthquakeCreate, EarthquakeUpdate
from app.repositories.earthquake_repository import (
    create_earthquake,
    get_all_earthquakes,
    get_earthquake_count,
    get_earthquake_by_id,
    update_earthquake,
    delete_earthquake
)

router = APIRouter(
    prefix="/api/v1/earthquakes",
    tags=["Earthquakes CRUD"]
)


@router.post("/")
def create(data: EarthquakeCreate):
    earthquake_id = create_earthquake(data)
    return {
        "status": "success",
        "message": "Earthquake created successfully",
        "id": earthquake_id
    }


@router.get("/")
def get_all(
    limit: int = Query(default=500, ge=1, le=5000, description="Jumlah data yang diambil"),
    offset: int = Query(default=0, ge=0, description="Offset untuk pagination")
):
    data = get_all_earthquakes(limit=limit, offset=offset)
    total = get_earthquake_count()
    return {
        "status": "success",
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": data
    }


@router.get("/{earthquake_id}")
def get_by_id(earthquake_id: int):
    data = get_earthquake_by_id(earthquake_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Earthquake not found")
    return {
        "status": "success",
        "data": data
    }


@router.put("/{earthquake_id}")
def update(earthquake_id: int, data: EarthquakeUpdate):
    update_earthquake(earthquake_id, data)
    return {
        "status": "success",
        "message": "Earthquake updated successfully"
    }


@router.delete("/{earthquake_id}")
def delete(earthquake_id: int):
    delete_earthquake(earthquake_id)
    return {
        "status": "success",
        "message": "Earthquake deleted successfully"
    }
