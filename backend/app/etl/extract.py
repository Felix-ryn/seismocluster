import requests

USGS_URL = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson"

def fetch_usgs_data():
    response = requests.get(USGS_URL)
    data = response.json()
    return data["features"]