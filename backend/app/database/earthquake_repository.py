from app.database.db_connection import get_cursor

def insert_earthquakes(data):
    conn, cursor = get_cursor()

    query = """
    INSERT INTO earthquakes (time, latitude, longitude, depth, magnitude, place)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    for row in data:
        cursor.execute(query, (
            row["time"],
            row["latitude"],
            row["longitude"],
            row["depth"],
            row["magnitude"],
            row["place"]
        ))

    conn.commit()
    cursor.close()
    conn.close()


def fetch_all_earthquakes():
    conn, cursor = get_cursor()

    cursor.execute("SELECT * FROM earthquakes")
    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data