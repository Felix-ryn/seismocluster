# filepath: backend/app/services/cluster_service.py
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text 

from app.models.pipeline import SeismoPipeline
from app.models.clustering.dbscan_model import DBSCANClustering
from app.models.clustering.kmeans_model import KMeansClustering
from app.models.clustering.evaluation import ClusterEvaluator
# IMPORT MODEL BARU: Isolation Forest
from app.models.anomaly.isolation_forest_model import IsolationForestAnomaly

class ClusterService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.pipeline = SeismoPipeline()
        self.dbscan = DBSCANClustering(eps=0.15, min_samples=15)
        self.kmeans = KMeansClustering(n_clusters=5) 
        # Inisialisasi Model Anomali
        self.iforest = IsolationForestAnomaly(contamination=0.01) 

    def execute_ml_pipeline(self):
        """Orkestrasi: Extract -> Transform -> Predict -> Load (ETL + ML + Anomaly)"""
        
        # 1. EXTRACT & TRANSFORM
        df = self.pipeline.load_from_db(self.db)
        if df.empty:
            return {"status": "error", "message": "Data gempa Indonesia kosong."}
            
        df = self.pipeline.prepare_features(df)
        self.pipeline.save_scaler() 

        # 2. PREDICT (Clustering & Anomaly Detection)
        # A. Clustering (Menggunakan 4 Dimensi: Lokasi, Kedalaman, Magnitudo)
        fitur_ml = df[['latitude_scaled', 'longitude_scaled', 'depth_scaled', 'magnitude_scaled']].values
        df['cluster_kmeans'] = self.kmeans.run(fitur_ml)
        df['cluster_label'] = self.dbscan.run(fitur_ml)
        df['is_noise'] = df['cluster_label'] == -1

        # B. Anomaly Detection (FOKUS pada 2 Dimensi: Kedalaman & Magnitudo Ekstrem)
        fitur_anomali = df[['depth_scaled', 'magnitude_scaled']].values
        df['is_anomaly'] = self.iforest.run(fitur_anomali)

        # Menghitung jumlah anomali untuk laporan di API
        total_anomali = int(df['is_anomaly'].sum())

        # 3. EVALUASI 
        eval_kmeans = ClusterEvaluator.evaluate_model("K-Means", fitur_ml, df['cluster_kmeans'].values)
        eval_dbscan = ClusterEvaluator.evaluate_model("DBSCAN", fitur_ml, df['cluster_label'].values)
        
        # 4. LOAD (Menyimpan ke PostgreSQL secara aman)
        try:
            connection = self.db.connection()
            connection.execute(text("TRUNCATE TABLE processed_earthquakes, earthquake_clusters, cluster_summary CASCADE;"))

            # A. Isi tabel `processed_earthquakes`
            cols_processed = [
                'id', 'time', 'latitude', 'longitude', 'depth', 'magnitude',
                'year', 'month', 'day',
                'latitude_scaled', 'longitude_scaled', 'depth_scaled', 'magnitude_scaled'
            ]
            df[cols_processed].to_sql('processed_earthquakes', con=connection, if_exists='append', index=False)

            # B. Isi tabel `earthquake_cluster`
            # CATATAN: Kita hanya menyimpan 'id', 'cluster_label', dan 'is_noise' sesuai ERD Anda saat ini.
            df_cluster = df[['id', 'cluster_label', 'is_noise']].copy()
            df_cluster.rename(columns={'id': 'ide'}, inplace=True)
            df_cluster['created_at'] = datetime.now()
            df_cluster.to_sql('earthquake_clusters', con=connection, if_exists='append', index=False)

            # C. Hitung & Isi tabel `cluster_summary`
            df_valid = df[df['cluster_label'] != -1]
            df_summary = df_valid.groupby('cluster_label').agg(
                total_earthquakes=('id', 'count'),
                avg_magnitude=('magnitude', 'mean'),
                avg_depth=('depth', 'mean')
            ).reset_index()
            df_summary.to_sql('cluster_summary', con=connection, if_exists='append', index=False)

            self.db.commit()

            # MENGEMBALIKAN RESPON API YANG KAYA (RICH RESPONSE)
            return {
                "status": "success",
                "summary": {
                    "total_data_processed": len(df),
                    "hotspot_zones_found": len(df_valid['cluster_label'].unique()),
                    "anomaly_alerts_detected": total_anomali # Info krusial untuk Halaman 5 Dashboard
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