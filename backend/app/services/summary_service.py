from app.config.database import get_connection


def get_summary():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT cluster_label, total_earthquakes, avg_magnitude, avg_depth
        FROM cluster_summary
        ORDER BY cluster_label ASC
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {
            "cluster": d[0],
            "total_earthquakes": d[1],
            "avg_magnitude": round(float(d[2]), 4) if d[2] else 0.0,
            "avg_depth": round(float(d[3]), 4) if d[3] else 0.0
        }
        for d in data
    ]


def get_summary_stats():
    """Statistik keseluruhan pipeline terakhir."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) as total_clusters,
            SUM(total_earthquakes) as total_earthquakes,
            AVG(avg_magnitude) as avg_magnitude,
            AVG(avg_depth) as avg_depth
        FROM cluster_summary
    """)
    stats = cur.fetchone()

    cur.execute("""
        SELECT COUNT(*) FROM earthquake_clusters WHERE is_anomaly = TRUE
    """)
    anomaly_row = cur.fetchone()

    cur.execute("""
        SELECT COUNT(*) FROM earthquake_clusters WHERE is_noise = TRUE
    """)
    noise_row = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total_clusters": int(stats[0]) if stats[0] else 0,
        "total_earthquakes_processed": int(stats[1]) if stats[1] else 0,
        "avg_magnitude": round(float(stats[2]), 4) if stats[2] else 0.0,
        "avg_depth": round(float(stats[3]), 4) if stats[3] else 0.0,
        "total_anomalies": int(anomaly_row[0]) if anomaly_row else 0,
        "total_noise_points": int(noise_row[0]) if noise_row else 0
    }
