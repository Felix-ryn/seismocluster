from app.config.database import get_connection

def get_earthquakes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT latitude, longitude, magnitude
        FROM processed_earthquakes
        LIMIT 1000
    """)

    data = cur.fetchall()
    cur.close()
    conn.close()

    return [{"lat": d[0], "lon": d[1], "mag": d[2]} for d in data]