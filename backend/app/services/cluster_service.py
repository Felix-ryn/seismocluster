import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.models.pipeline import SeismoPipeline
from app.models.clustering.dbscan_model import DBSCANClustering
from app.models.clustering.kmeans_model import KMeansClustering
from app.models.clustering.evaluation import ClusterEvaluator
from app.models.anomaly.isolation_forest_model import IsolationForestAnomaly
from app.etl.pipeline import run_pipeline as run_etl


class ClusterService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.pipeline = SeismoPipeline()
        self.dbscan = DBSCANClustering(eps=0.15, min_samples=15)
        self.kmeans = KMeansClustering(n_clusters=5)
        self.iforest = IsolationForestAnomaly(contamination=0.01)

    def run_etl_pipeline(self):
        """Ambil data terbaru dari USGS dan simpan ke raw_earthquakes."""
        run_etl()
        return {"status": "success", "message": "Data gempa berhasil diambil dari USGS"}

    def execute_ml_pipeline(self):
        """Orkestrasi: Extract -> Transform -> Predict -> Load (ETL + ML + Anomaly)"""

        # 1. EXTRACT & TRANSFORM
        df = self.pipeline.load_from_db(self.db)

        if df.empty:
            return {"status": "error", "message": "Data gempa Indonesia kosong. Jalankan POST /clusters/etl terlebih dahulu."}

        N_CLUSTERS = 5
        if len(df) < N_CLUSTERS:
            return {
                "status": "error",
                "message": f"Data gempa Indonesia terlalu sedikit: hanya {len(df)} record. "
                           f"Minimal {N_CLUSTERS} data diperlukan untuk K-Means (n_clusters={N_CLUSTERS}). "
                           "Jalankan POST /clusters/etl untuk menambah data."
            }

        df = self.pipeline.prepare_features(df, is_training=True)

        # 2. PREDICT (Clustering & Anomaly Detection)
        # Sesuaikan n_clusters jika data masih kurang dari 5 setelah prepare_features
        n_clusters_actual = min(N_CLUSTERS, len(df))
        if n_clusters_actual != N_CLUSTERS:
            self.kmeans = KMeansClustering(n_clusters=n_clusters_actual)

        fitur_ml = df[['latitude_scaled', 'longitude_scaled', 'depth_scaled', 'magnitude_scaled']].values
        df['cluster_kmeans'] = self.kmeans.run(fitur_ml)
        df['cluster_label'] = self.dbscan.run(fitur_ml)
        df['is_noise'] = df['cluster_label'] == -1

        fitur_anomali = df[['depth_scaled', 'magnitude_scaled']].values
        df['is_anomaly'] = self.iforest.run(fitur_anomali)
        total_anomali = int(df['is_anomaly'].sum())

        # 3. EVALUASI
        eval_kmeans = ClusterEvaluator.evaluate_model("K-Means", fitur_ml, df['cluster_kmeans'].values)
        eval_dbscan = ClusterEvaluator.evaluate_model("DBSCAN", fitur_ml, df['cluster_label'].values)

        # 4. LOAD ke PostgreSQL
        try:
            connection = self.db.connection()
            connection.execute(text("TRUNCATE TABLE processed_earthquakes, earthquake_clusters, cluster_summary CASCADE;"))

            # A. Tabel processed_earthquakes (13 kolom sesuai schema DB)
            cols_processed = [
                'id', 'time', 'latitude', 'longitude', 'depth', 'magnitude',
                'year', 'month', 'day',
                'latitude_scaled', 'longitude_scaled', 'depth_scaled', 'magnitude_scaled'
            ]
            df[cols_processed].to_sql('processed_earthquakes', con=connection, if_exists='append', index=False)

            # B. cluster_summary dari K-Means (lebih stabil dari DBSCAN untuk data Indonesia)
            # cluster_label di sini pakai cluster_kmeans bukan DBSCAN
            df_summary = df.groupby('cluster_kmeans').agg(
                total_earthquakes=('id', 'count'),
                avg_magnitude=('magnitude', 'mean'),
                avg_depth=('depth', 'mean')
            ).reset_index()
            df_summary.rename(columns={'cluster_kmeans': 'cluster_label'}, inplace=True)
            df_summary.to_sql('cluster_summary', con=connection, if_exists='append', index=False)

            # C. earthquake_clusters — gunakan K-Means sebagai cluster_label utama
            # DBSCAN disimpan di is_noise; noise DBSCAN tidak menjadi cluster_label FK
            df_cluster = df[['id', 'cluster_kmeans', 'is_noise', 'is_anomaly']].copy()
            df_cluster.rename(columns={'cluster_kmeans': 'cluster_label'}, inplace=True)
            df_cluster['created_at'] = datetime.now()
            df_cluster.to_sql('earthquake_clusters', con=connection, if_exists='append', index=False)

            self.db.commit()

            return {
                "status": "success",
                "summary": {
                    "total_data_processed": len(df),
                    "hotspot_zones_found": int(df['cluster_kmeans'].nunique()),
                    "anomaly_alerts_detected": total_anomali
                },
                "evaluation_metrics": {
                    "kmeans": eval_kmeans,
                    "dbscan": eval_dbscan
                }
            }

        except Exception as e:
            self.db.rollback()
            print(f"Database Error: {e}")
            raise e
