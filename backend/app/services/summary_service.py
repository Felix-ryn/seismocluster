from app.config.database import get_connection

def get_summary():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT cluster_label, total_earthquakes, avg_magnitude
        FROM cluster_summary
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()

    return [
        {"cluster": d[0], "total": d[1], "avg_mag": d[2]}
        for d in data
    ]