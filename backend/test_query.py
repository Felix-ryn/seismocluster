from app.config.database import get_cursor

try:
    conn, cursor = get_cursor()

    cursor.execute("SELECT version();")
    result = cursor.fetchone()

    print("✅ Koneksi OK")
    print("PostgreSQL Version:", result)

    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Error:", e)