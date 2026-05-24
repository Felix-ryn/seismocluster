import requests
import os
from datetime import datetime

COMCAT_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

# Bounding box Indonesia — filter langsung di API, bukan setelah masuk DB
LAT_MIN, LAT_MAX = -11.0,  6.0
LON_MIN, LON_MAX =  95.0, 141.0

# Tahun mulai historis (bisa di-override via env)
HISTORICAL_START_YEAR = int(os.getenv("ETL_START_YEAR", "2010"))


def _month_chunks(start: datetime, end: datetime):
    """Yield (chunk_start, chunk_end) per bulan kalender."""
    current = start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    while current < end:
        if current.month == 12:
            next_m = current.replace(year=current.year + 1, month=1)
        else:
            next_m = current.replace(month=current.month + 1)
        yield current, min(next_m, end)
        current = next_m


def fetch_usgs_data(start_date: datetime = None) -> list:
    """
    Ambil gempa Indonesia dari USGS ComCat API.

    - start_date=None  → full historical backfill dari ETL_START_YEAR sampai sekarang
    - start_date=dt    → incremental: ambil dari dt sampai sekarang

    Chunking per bulan agar tidak melebihi limit 20.000 record/request.
    Filter bounding box Indonesia dilakukan langsung di API (lebih efisien).
    """
    if start_date is None:
        start_date = datetime(HISTORICAL_START_YEAR, 1, 1)
        print(f"Mode: Full historical backfill dari {HISTORICAL_START_YEAR}")
    else:
        print(f"Mode: Incremental dari {start_date.strftime('%Y-%m-%d')}")

    end_date = datetime.utcnow()
    all_features = []
    total_chunks = 0

    for chunk_start, chunk_end in _month_chunks(start_date, end_date):
        total_chunks += 1
        params = {
            "format":       "geojson",
            "starttime":    chunk_start.strftime("%Y-%m-%dT%H:%M:%S"),
            "endtime":      chunk_end.strftime("%Y-%m-%dT%H:%M:%S"),
            "minlatitude":  LAT_MIN,
            "maxlatitude":  LAT_MAX,
            "minlongitude": LON_MIN,
            "maxlongitude": LON_MAX,
            "limit":        20000,
            "orderby":      "time-asc",
        }

        try:
            response = requests.get(COMCAT_URL, params=params, timeout=60)
            response.raise_for_status()
            features = response.json().get("features", [])
            all_features.extend(features)
            print(f"  [{chunk_start.strftime('%Y-%m')}] {len(features)} gempa")
        except Exception as e:
            print(f"  [{chunk_start.strftime('%Y-%m')}] Error: {e} — skip")

    print(f"Total: {len(all_features)} gempa dari {total_chunks} chunk")
    return all_features
