from app.repositories.earthquake_repository import insert_earthquakes_bulk

def load_to_database(data):
    return insert_earthquakes_bulk(data)
