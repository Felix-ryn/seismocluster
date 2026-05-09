from app.repositories.earthquake_repository import (
    create_earthquake,
    get_all_earthquakes,
    get_earthquake_by_id,
    update_earthquake,
    delete_earthquake
)


def create_earthquake_service(data):
    return create_earthquake(data)


def get_all_earthquakes_service():
    return get_all_earthquakes()


def get_earthquake_by_id_service(earthquake_id):
    return get_earthquake_by_id(earthquake_id)


def update_earthquake_service(earthquake_id, data):
    return update_earthquake(earthquake_id, data)


def delete_earthquake_service(earthquake_id):
    return delete_earthquake(earthquake_id)