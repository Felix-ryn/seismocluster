from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.pipeline import SeismoPipeline
from app.etl.pipeline import run_pipeline as run_etl
from app.services.ml_service import run_clustering


class ClusterService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.pipeline = SeismoPipeline()

    def run_etl_pipeline(self):
        """Ambil data terbaru dari USGS dan simpan ke raw_earthquakes."""
        inserted = run_etl()
        return {
            "status": "success",
            "message": "Data gempa berhasil diambil dari USGS",
            "inserted_count": inserted
        }

    def execute_ml_pipeline(self):
        """
        Orkestrasi penuh:
          1. Load raw_earthquakes → preprocessing → simpan ke processed_earthquakes
          2. ml_service.run_clustering() → baca processed_earthquakes
             → predict MLflow @champion → simpan ke earthquake_clusters + cluster_summary
        """

        # 1. LOAD dari raw_earthquakes (Indonesia only)
        df = self.pipeline.load_from_db(self.db)

        if df.empty:
            return {
                "status": "error",
                "message": "Data gempa Indonesia kosong. Jalankan POST /clusters/etl terlebih dahulu."
            }

        # 2. PREPROCESSING — fit scaler baru, tambah fitur temporal & scaled
        df = self.pipeline.prepare_features(df, is_training=True)

        # 3. TRUNCATE semua result tables lalu simpan ke processed_earthquakes
        try:
            connection = self.db.connection()
            connection.execute(text(
                "ALTER TABLE earthquake_clusters ADD COLUMN IF NOT EXISTS hierarchy_label INTEGER;"
            ))
            connection.execute(text(
                "TRUNCATE TABLE processed_earthquakes, earthquake_clusters, cluster_summary CASCADE;"
            ))

            cols_processed = [
                'id', 'time', 'latitude', 'longitude', 'depth', 'magnitude',
                'year', 'month', 'day',
                'latitude_scaled', 'longitude_scaled', 'depth_scaled', 'magnitude_scaled'
            ]
            df[cols_processed].to_sql(
                'processed_earthquakes', con=connection, if_exists='append', index=False
            )
            self.db.commit()

        except Exception as e:
            self.db.rollback()
            print(f"Database Error (preprocessing): {e}")
            raise e

        # 4. ML: baca processed_earthquakes → predict → simpan hasil
        return run_clustering(self.db)
