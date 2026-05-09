from datetime import datetime

def transform_data(features):
    cleaned = []

    for item in features:
        props = item["properties"]
        coords = item["geometry"]["coordinates"]

        cleaned.append({
            "time": datetime.utcfromtimestamp(props["time"] / 1000),
            "latitude": coords[1],
            "longitude": coords[0],
            "depth": coords[2],
            "magnitude": props["mag"],
            "place": props["place"]
        })

    return cleaned