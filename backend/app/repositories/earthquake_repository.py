from app.config.database import get_cursor


def create_earthquake(data):

    conn, cursor = get_cursor()

    query = """
    INSERT INTO raw_earthquakes
    (
        time,
        latitude,
        longitude,
        depth,
        magnitude,
        place
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id
    """

    cursor.execute(query, (
        data.time,
        data.latitude,
        data.longitude,
        data.depth,
        data.magnitude,
        data.place
    ))

    earthquake_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return earthquake_id


def get_all_earthquakes():

    conn, cursor = get_cursor()

    cursor.execute("""
        SELECT *
        FROM raw_earthquakes
        ORDER BY time DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def get_earthquake_by_id(earthquake_id):

    conn, cursor = get_cursor()

    cursor.execute("""
        SELECT *
        FROM raw_earthquakes
        WHERE id = %s
    """, (earthquake_id,))

    data = cursor.fetchone()

    cursor.close()
    conn.close()

    return data


def delete_earthquake(earthquake_id):

    conn, cursor = get_cursor()

    cursor.execute("""
        DELETE FROM raw_earthquakes
        WHERE id = %s
    """, (earthquake_id,))

    conn.commit()

    cursor.close()
    conn.close()

    return True

def update_earthquake(earthquake_id, data):

    conn, cursor = get_cursor()

    query = """
    UPDATE raw_earthquakes
    SET
        time = %s,
        latitude = %s,
        longitude = %s,
        depth = %s,
        magnitude = %s,
        place = %s
    WHERE id = %s
    """

    cursor.execute(query, (
        data.time,
        data.latitude,
        data.longitude,
        data.depth,
        data.magnitude,
        data.place,
        earthquake_id
    ))

    conn.commit()

    cursor.close()
    conn.close()

    return True