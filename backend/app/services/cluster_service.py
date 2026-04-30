# filepath: backend/app/services/cluster_service.py
import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import text # Tambahan untuk eksekusi query raw
from app.models.clustering.pipeline import SeismoDataPipeline # Perbaikan import
from app.models.clustering.dbscan_model import DBSCANClustering
from app.models.clustering.kmeans_model import KMeansClustering # Import K-Means

class ClusterService:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.pipeline = SeismoDataPipeline()
        self.dbscan = DBSCANClustering(eps=0.15, min_samples=15)
        self.kmeans = KMeansClustering(n_clusters=5) # Inisialisasi K-Means

    def execute_ml_pipeline(self):
        """Orkestrasi: Extract -> Transform -> Predict -> Load (ETL + ML)"""
        
        # 1. EXTRACT & TRANSFORM
        df = self.pipeline.load_from_db(self.db)
        if df.empty:
            return {"status": "error", "message": "Data gempa Indonesia kosong."}
            
        df = self.pipeline.prepare_features(df)

        # 2. PREDICT (Menjalankan Machine Learning)
        fitur_ml = df[['latitude_scaled', 'longitude_scaled', 'depth_scaled', 'magnitude_scaled']].values
        
        # Eksekusi K-Means & DBSCAN (Kedua model jalan sesuai target Minggu 10)
        df['cluster_kmeans'] = self.kmeans.run(fitur_ml)
        df['cluster_label'] = self.dbscan.run(fitur_ml) # cluster_label default pakai DBSCAN
        
        df['is_noise'] = df['cluster_label'] == -1

        # 3. LOAD (Menyimpan ke PostgreSQL secara aman)
        try:
            # AMAN UNTUK ERD: Kosongkan isi tabel tanpa menghapus struktur/relasinya
            # CASCADE memastikan relasi Foreign Key dibersihkan secara berurutan
            self.db.execute(text("TRUNCATE TABLE processed_earthquakes, earthquake_cluster, cluster_summary CASCADE;"))
            self.db.commit()

            # A. Isi tabel `processed_earthquakes`
            cols_processed = [
                'id', 'time', 'latitude', 'longitude', 'depth', 'magnitude',
                'year', 'month', 'day',
                'latitude_scaled', 'longitude_scaled', 'depth_scaled', 'magnitude_scaled'
            ]
            # Gunakan 'append', BUKAN 'replace'
            df[cols_processed].to_sql('processed_earthquakes', con=self.db.bind, if_exists='append', index=False)

            # B. Isi tabel `earthquake_cluster`
            df_cluster = df[['id', 'cluster_label', 'is_noise']].copy()
            df_cluster.rename(columns={'id': 'ide'}, inplace=True)
            df_cluster['created_at'] = datetime.now()
            df_cluster.to_sql('earthquake_cluster', con=self.db.bind, if_exists='append', index=False)

            # C. Hitung & Isi tabel `cluster_summary`
            df_valid = df[df['cluster_label'] != -1]
            df_summary = df_valid.groupby('cluster_label').agg(
                total_earthquakes=('id', 'count'),
                avg_magnitude=('magnitude', 'mean'),
                avg_depth=('depth', 'mean')
            ).reset_index()
            df_summary.to_sql('cluster_summary', con=self.db.bind, if_exists='append', index=False)

            return {
                "status": "success",
                "processed_rows": len(df),
                "hotspot_zones_found": len(df_summary)
            }

        except Exception as e:
            self.db.rollback() # Jika terjadi error, kembalikan state database
            print(f"Database Error: {e}")
            raise e