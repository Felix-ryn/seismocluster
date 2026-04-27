from app.config.database import get_connection

def get_clusters():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT p.latitude, p.longitude, c.cluster_label
        FROM processed_earthquakes p
        JOIN earthquake_clusters c ON p.id = c.id
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()

    return [{"lat": d[0], "lon": d[1], "cluster": d[2]} for d in data]