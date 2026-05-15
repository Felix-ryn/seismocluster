from app.config.database import get_cursor


def create_earthquake(data):
    conn, cursor = get_cursor()
    query = """
    INSERT INTO raw_earthquakes
    (time, latitude, longitude, depth, magnitude, place)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    cursor.execute(query, (
        data.time, data.latitude, data.longitude,
        data.depth, data.magnitude, data.place
    ))
    earthquake_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return earthquake_id


def insert_earthquakes_bulk(data_list):
    """
    Bulk insert dari ETL pipeline USGS.
    Kolom yang diisi: time, latitude, longitude, depth, magnitude,
                      mag_type, nst, gap, dmin, rms, net, place, type,
                      horizontal_error, depth_error, mag_error, mag_nst,
                      status, location_source, mag_source, updated
    """
    conn, cursor = get_cursor()

    query = """
    INSERT INTO raw_earthquakes (
        id,
        time, latitude, longitude, depth, magnitude,
        mag_type, nst, gap, dmin, rms, net, place, type,
        horizontal_error, depth_error, mag_error, mag_nst,
        status, location_source, mag_source, updated
    )
    VALUES (
        %s,
        %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s,
        %s, %s, %s, %s
    )
    ON CONFLICT (id) DO NOTHING
    """

    values = [
        (
            d.get('id'),
            d.get('time'),
            d.get('latitude'),
            d.get('longitude'),
            d.get('depth'),
            d.get('magnitude'),
            d.get('mag_type'),
            d.get('nst'),
            d.get('gap'),
            d.get('dmin'),
            d.get('rms'),
            d.get('net'),
            d.get('place'),
            d.get('type'),
            d.get('horizontal_error'),
            d.get('depth_error'),
            d.get('mag_error'),
            d.get('mag_nst'),
            d.get('status'),
            d.get('location_source'),
            d.get('mag_source'),
            d.get('updated'),
        )
        for d in data_list
        if d.get('magnitude') is not None and d.get('id') is not None
    ]

    cursor.executemany(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return len(values)


def get_all_earthquakes(limit=500, offset=0, indonesia_only=False):
    conn, cursor = get_cursor()
    where = """
        WHERE latitude BETWEEN -11.0 AND 6.0
          AND longitude BETWEEN 95.0 AND 141.0
    """ if indonesia_only else ""
    cursor.execute(f"""
        SELECT
            id, time, latitude, longitude, depth, magnitude,
            mag_type, place, status, updated
        FROM raw_earthquakes
        {where}
        ORDER BY time DESC
        LIMIT %s OFFSET %s
    """, (limit, offset))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(row) for row in data]


def get_earthquake_count(indonesia_only=False):
    conn, cursor = get_cursor()
    where = """
        WHERE latitude BETWEEN -11.0 AND 6.0
          AND longitude BETWEEN 95.0 AND 141.0
    """ if indonesia_only else ""
    cursor.execute(f"SELECT COUNT(*) as total FROM raw_earthquakes {where}")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['total']


def get_earthquake_by_id(earthquake_id):
    conn, cursor = get_cursor()
    cursor.execute("""
        SELECT * FROM raw_earthquakes WHERE id = %s
    """, (earthquake_id,))
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return dict(data) if data else None


def update_earthquake(earthquake_id, data):
    conn, cursor = get_cursor()

    fields = []
    values = []

    if data.time is not None:
        fields.append("time = %s")
        values.append(data.time)
    if data.latitude is not None:
        fields.append("latitude = %s")
        values.append(data.latitude)
    if data.longitude is not None:
        fields.append("longitude = %s")
        values.append(data.longitude)
    if data.depth is not None:
        fields.append("depth = %s")
        values.append(data.depth)
    if data.magnitude is not None:
        fields.append("magnitude = %s")
        values.append(data.magnitude)
    if data.place is not None:
        fields.append("place = %s")
        values.append(data.place)

    if not fields:
        cursor.close()
        conn.close()
        return True

    values.append(earthquake_id)
    query = f"UPDATE raw_earthquakes SET {', '.join(fields)} WHERE id = %s"
    cursor.execute(query, tuple(values))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def delete_earthquake(earthquake_id):
    conn, cursor = get_cursor()
    cursor.execute("DELETE FROM raw_earthquakes WHERE id = %s", (earthquake_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_cluster_results(limit=500, offset=0):
    """
    Hasil clustering: join earthquake_clusters dengan raw_earthquakes.
    earthquake_clusters.id = FK ke raw_earthquakes.id
    """
    conn, cursor = get_cursor()
    cursor.execute("""
        SELECT
            re.id,
            re.time,
            re.latitude,
            re.longitude,
            re.depth,
            re.magnitude,
            re.place,
            ec.cluster_label,
            ec.is_noise,
            ec.is_anomaly,
            ec.created_at
        FROM earthquake_clusters ec
        JOIN raw_earthquakes re ON ec.id = re.id
        ORDER BY ec.created_at DESC
        LIMIT %s OFFSET %s
    """, (limit, offset))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(row) for row in data]


def get_cluster_result_count():
    conn, cursor = get_cursor()
    cursor.execute("SELECT COUNT(*) as total FROM earthquake_clusters")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result['total']


def get_anomaly_earthquakes(limit=200):
    """
    Gempa yang terdeteksi sebagai anomali (kedalaman/magnitudo ekstrem).
    Memerlukan kolom is_anomaly di earthquake_clusters:
      ALTER TABLE earthquake_clusters ADD COLUMN is_anomaly BOOLEAN DEFAULT FALSE;
    """
    conn, cursor = get_cursor()
    cursor.execute("""
        SELECT
            re.id,
            re.time,
            re.latitude,
            re.longitude,
            re.depth,
            re.magnitude,
            re.place,
            ec.cluster_label,
            ec.is_anomaly
        FROM earthquake_clusters ec
        JOIN raw_earthquakes re ON ec.id = re.id
        WHERE ec.is_anomaly = TRUE
        ORDER BY re.magnitude DESC
        LIMIT %s
    """, (limit,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return [dict(row) for row in data]
