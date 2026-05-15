import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.pipeline import SeismoPipeline
from app.models.clustering.evaluation import ClusterEvaluator
from app.etl.pipeline import run_pipeline as run_etl


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
        """Orkestrasi: Load -> Preprocess -> Predict (MLflow champion) -> Save ke DB"""

        # 1. LOAD DATA (semua data Indonesia, tanpa limit)
        df = self.pipeline.load_from_db(self.db)

        if df.empty:
            return {
                "status": "error",
                "message": "Data gempa Indonesia kosong. Jalankan POST /clusters/etl terlebih dahulu."
            }

        # 2. PREPROCESSING — fit scaler baru dari data saat ini
        df = self.pipeline.prepare_features(df, is_training=True)

        # 3. PREDICT menggunakan model MLflow @champion
        #    (Hierarchical Clustering + Isolation Forest)
        df = self.pipeline.predict_all(df)
        total_anomali = int(df['is_anomaly'].sum())

        # 4. EVALUASI Hierarchical clustering menggunakan koordinat radian
        coords_radians = df[['lat_radian', 'lon_radian']].values
        eval_result = ClusterEvaluator.evaluate_model(
            "Hierarchical (MLflow Champion)",
            coords_radians,
            df['zona_klaster'].values
        )

        # 5. SAVE ke PostgreSQL
        try:
            connection = self.db.connection()
            connection.execute(text(
                "TRUNCATE TABLE processed_earthquakes, earthquake_clusters, cluster_summary CASCADE;"
            ))

            # A. processed_earthquakes
            cols_processed = [
                'id', 'time', 'latitude', 'longitude', 'depth', 'magnitude',
                'year', 'month', 'day',
                'latitude_scaled', 'longitude_scaled', 'depth_scaled', 'magnitude_scaled'
            ]
            df[cols_processed].to_sql(
                'processed_earthquakes', con=connection, if_exists='append', index=False
            )

            # B. cluster_summary — berdasarkan zona_klaster dari Hierarchical
            df_summary = df.groupby('zona_klaster').agg(
                total_earthquakes=('id', 'count'),
                avg_magnitude=('magnitude', 'mean'),
                avg_depth=('depth', 'mean')
            ).reset_index()
            df_summary.rename(columns={'zona_klaster': 'cluster_label'}, inplace=True)
            df_summary.to_sql(
                'cluster_summary', con=connection, if_exists='append', index=False
            )

            # C. earthquake_clusters
            # Hierarchical tidak mengenal noise, semua titik masuk cluster
            df_cluster = df[['id', 'zona_klaster', 'is_anomaly']].copy()
            df_cluster.rename(columns={'zona_klaster': 'cluster_label'}, inplace=True)
            df_cluster['is_noise'] = False
            df_cluster['created_at'] = datetime.now()
            df_cluster.to_sql(
                'earthquake_clusters', con=connection, if_exists='append', index=False
            )

            self.db.commit()

            return {
                "status": "success",
                "model_source": "MLflow @champion (Hierarchical + Isolation Forest)",
                "summary": {
                    "total_data_processed": len(df),
                    "hotspot_zones_found": int(df['zona_klaster'].nunique()),
                    "anomaly_alerts_detected": total_anomali
                },
                "evaluation_metrics": {
                    "hierarchical": eval_result
                }
            }

        except Exception as e:
            self.db.rollback()
            print(f"Database Error: {e}")
            raise e
