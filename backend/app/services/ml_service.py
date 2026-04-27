import pandas as pd
from app.config.database import get_connection
from app.models.pipeline import run_pipeline

def run_clustering():
    conn = get_connection()

    df = pd.read_sql("SELECT * FROM processed_earthquakes", conn)

    df = run_pipeline(df)

    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("""
            INSERT INTO earthquake_clusters (id, cluster_label, is_noise)
            VALUES (%s, %s, %s)
            ON CONFLICT (id) DO UPDATE
            SET cluster_label = EXCLUDED.cluster_label,
                is_noise = EXCLUDED.is_noise
        """, (row["id"], int(row["cluster_label"]), bool(row["is_noise"])))

    conn.commit()
    cur.close()
    conn.close()

    return {"status": "clustering done"}