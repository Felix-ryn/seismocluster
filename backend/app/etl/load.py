from app.database.earthquake_repository import insert_earthquakes

def load_to_database(data):
    insert_earthquakes(data)