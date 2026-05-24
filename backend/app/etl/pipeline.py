from datetime import timedelta

from app.etl.extract import fetch_usgs_data
from app.etl.transform import transform_data
from app.etl.load import load_to_database
from app.repositories.earthquake_repository import get_latest_earthquake_time


def run_pipeline():
    print("Starting ETL Pipeline...")

    # Cek data terakhir di DB
    latest = get_latest_earthquake_time()

    if latest:
        # Incremental: mulai dari 2 hari sebelum data terakhir
        # (overlap 2 hari untuk antisipasi data telat masuk ke USGS)
        start_date = latest - timedelta(days=2)
        print(f"Incremental update dari {start_date.strftime('%Y-%m-%d')} (overlap 2 hari)")
    else:
        # DB kosong: full historical backfill
        start_date = None
        print("Database kosong — full historical backfill...")

    raw_data = fetch_usgs_data(start_date)
    print(f"Extracted: {len(raw_data)} records")

    transformed = transform_data(raw_data)
    print(f"Transformed: {len(transformed)} records")

    # ON CONFLICT DO NOTHING — duplikat dari overlap diabaikan otomatis
    inserted = load_to_database(transformed)
    print(f"Data loaded: {inserted} baru disimpan")

    print("ETL Pipeline finished!")
    return inserted
