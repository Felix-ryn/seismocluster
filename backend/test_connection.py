from app.config.database import get_connection

try:
    conn = get_connection()
    print("✅ Berhasil konek ke database!")

    conn.close()

except Exception as e:
    print("❌ Gagal konek ke database")
    print("Error:", e)