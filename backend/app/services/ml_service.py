import pandas as pd
from app.config.database import get_connection
from app.models.clustering.kmeans_model import KMeansClustering
from app.models.clustering.dbscan_model import DBSCANClustering
from app.models.anomaly.isolation_forest_model import IsolationForestAnomaly


def run_clustering():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM processed_earthquakes", conn)

    if df.empty:
        return {"status": "error", "message": "Tidak ada data di processed_earthquakes"}

    fitur = df[['latitude_scaled', 'longitude_scaled', 'depth_scaled', 'magnitude_scaled']].values

    kmeans = KMeansClustering(n_clusters=5)
    dbscan = DBSCANClustering(eps=0.15, min_samples=15)
    iforest = IsolationForestAnomaly(contamination=0.01)

    df['cluster_kmeans'] = kmeans.run(fitur)
    df['cluster_label'] = dbscan.run(fitur)
    df['is_noise'] = df['cluster_label'] == -1
    df['is_anomaly'] = iforest.run(df[['depth_scaled', 'magnitude_scaled']].values)

    cur = conn.cursor()
    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO earthquake_clusters (ide, cluster_label, is_noise, is_anomaly)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (ide) DO UPDATE
            SET cluster_label = EXCLUDED.cluster_label,
                is_noise = EXCLUDED.is_noise,
                is_anomaly = EXCLUDED.is_anomaly
        """, (row["id"], int(row["cluster_label"]), bool(row["is_noise"]), bool(row["is_anomaly"])))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "clustering done", "total": len(df)}
