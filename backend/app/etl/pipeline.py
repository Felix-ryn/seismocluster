from app.etl.extract import fetch_usgs_data
from app.etl.transform import transform_data
from app.etl.load import load_to_database

def run_pipeline():
    print("🚀 Starting ETL Pipeline...")

    raw_data = fetch_usgs_data()
    print(f"📥 Extracted: {len(raw_data)} records")

    transformed = transform_data(raw_data)
    print(f"🔄 Transformed: {len(transformed)} records")

    load_to_database(transformed)
    print("💾 Data loaded to database")

    print("✅ ETL Pipeline finished!")