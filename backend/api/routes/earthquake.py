from fastapi import APIRouter

from app.schemas.earthquake_schema import (
    EarthquakeCreate,
    EarthquakeUpdate
)

from app.services.earthquake_service import (
    create_earthquake_service,
    get_all_earthquakes_service,
    get_earthquake_by_id_service,
    update_earthquake_service,
    delete_earthquake_service
)

router = APIRouter(
    prefix="/api/v1/earthquakes",
    tags=["Earthquakes CRUD"]
)


@router.post("/")
def create(data: EarthquakeCreate):

    earthquake_id = create_earthquake_service(data)

    return {
        "status": "success",
        "message": "Earthquake created successfully",
        "id": earthquake_id
    }


@router.get("/")
def get_all():

    data = get_all_earthquakes_service()

    return {
        "status": "success",
        "data": data
    }


@router.get("/{earthquake_id}")
def get_by_id(earthquake_id: int):

    data = get_earthquake_by_id_service(earthquake_id)

    return {
        "status": "success",
        "data": data
    }


@router.put("/{earthquake_id}")
def update(earthquake_id: int, data: EarthquakeUpdate):

    update_earthquake_service(earthquake_id, data)

    return {
        "status": "success",
        "message": "Earthquake updated successfully"
    }


@router.delete("/{earthquake_id}")
def delete(earthquake_id: int):

    delete_earthquake_service(earthquake_id)

    return {
        "status": "success",
        "message": "Earthquake deleted successfully"
    }