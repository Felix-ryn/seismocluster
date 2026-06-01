import pandas as pd
import numpy as np
from datetime import datetime
from sqlalchemy.orm import Session
from app.models.pipeline import SeismoPipeline
from app.models.clustering.evaluation import ClusterEvaluator

def run_clustering(db: Session) -> dict:
    """
    Baca dari processed_earthquakes, jalankan model dari local joblib,
    simpan hasil ke earthquake_clusters dan cluster_summary.
    """
    pipeline = SeismoPipeline()
    connection = db.connection()

    # 1. READ dari processed_earthquakes
    df = pd.read_sql(
        "SELECT * FROM processed_earthquakes ORDER BY time DESC",
        con=connection
    )

    if df.empty:
        return {
            "status": "error",
            "message": "Tidak ada data di processed_earthquakes. Jalankan ETL dan training terlebih dahulu."
        }

    # 2. PREDICT menggunakan Local Joblib
    df = pipeline.predict_all(df)

    total_anomali = int(df['is_anomaly'].sum())

    # 3. EVALUASI
    coords_radians = df[['lat_radian', 'lon_radian']].values

    eval_kmeans = ClusterEvaluator.evaluate_model(
        "KMeans (Local Joblib)",
        coords_radians,
        df['zona_klaster'].values
    )

    eval_hierarchy = ClusterEvaluator.evaluate_model(
        "Hierarchical (Local Joblib)",
        coords_radians,
        df['hierarchy_label'].values
    )

    # 4. SAVE hasil ke cluster_summary dan earthquake_clusters
    try:
        df_summary = df.groupby('zona_klaster').agg(
            total_earthquakes=('id', 'count'),
            avg_magnitude=('magnitude', 'mean'),
            avg_depth=('depth', 'mean')
        ).reset_index()

        df_summary.rename(columns={'zona_klaster': 'cluster_label'}, inplace=True)
        df_summary.to_sql(
            'cluster_summary', con=connection, if_exists='append', index=False
        )

        df_cluster = df[['id', 'zona_klaster', 'hierarchy_label', 'is_anomaly']].copy()
        df_cluster.rename(columns={'zona_klaster': 'cluster_label'}, inplace=True)
        df_cluster['is_noise'] = False
        df_cluster['created_at'] = datetime.now()
        df_cluster.to_sql(
            'earthquake_clusters', con=connection, if_exists='append', index=False
        )

        db.commit()

        return {
            "status": "success",
            "model_source": "Local Joblib (KMeans + Hotspot + Isolation Forest + Hierarchical)",
            "summary": {
                "total_data_processed": len(df),
                "kmeans_zones_found": int(df['zona_klaster'].nunique()),
                "hotspot_zones_found": int(df['hotspot_zone'].nunique()),
                "hierarchy_zones_found": int(df['hierarchy_label'].nunique()),
                "anomaly_alerts_detected": total_anomali
            },
            "evaluation_metrics": {
                "kmeans": eval_kmeans,
                "hierarchical": eval_hierarchy
            }
        }

    except Exception as e:
        db.rollback()
        print(f"Database Error (ml_service): {e}")
        raise e