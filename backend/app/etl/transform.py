from datetime import datetime, timezone


def transform_data(features):
    """
    Transform GeoJSON dari USGS ke format sesuai schema raw_earthquakes (22 kolom).
    Kolom yang diisi dari USGS: time, latitude, longitude, depth, magnitude,
    mag_type, nst, gap, dmin, rms, net, place, type,
    horizontal_error, depth_error, mag_error, mag_nst, status,
    location_source, mag_source, updated
    """
    cleaned = []

    for item in features:
        props = item.get("properties", {})
        coords = item.get("geometry", {}).get("coordinates", [None, None, None])

        # USGS event ID (contoh: "us6000snye") — wajib ada di raw_earthquakes.id
        usgs_id = item.get("id")
        if not usgs_id:
            continue

        # Waktu: dari millisecond timestamp UTC
        raw_time = props.get("time")
        event_time = datetime.fromtimestamp(raw_time / 1000, tz=timezone.utc).replace(tzinfo=None) if raw_time else None

        raw_updated = props.get("updated")
        updated_time = datetime.fromtimestamp(raw_updated / 1000, tz=timezone.utc).replace(tzinfo=None) if raw_updated else None

        cleaned.append({
            "id": usgs_id,
            "time": event_time,
            "latitude": coords[1],
            "longitude": coords[0],
            "depth": coords[2],
            "magnitude": props.get("mag"),
            "mag_type": props.get("magType"),
            "nst": props.get("nst"),
            "gap": props.get("gap"),
            "dmin": props.get("dmin"),
            "rms": props.get("rms"),
            "net": props.get("net"),
            "place": props.get("place"),
            "type": props.get("type"),
            "horizontal_error": props.get("horizontalError"),
            "depth_error": props.get("depthError"),
            "mag_error": props.get("magError"),
            "mag_nst": props.get("magNst"),
            "status": props.get("status"),
            "location_source": props.get("locationSource"),
            "mag_source": props.get("magSource"),
            "updated": updated_time,
        })

    return cleaned
