# filepath: backend/app/config/database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Memuat variabel dari file .env
load_dotenv()

# Mengambil kredensial dari environment variables Anda
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", "5432") # Default 5432 jika kosong
DB_NAME = os.getenv("DB_NAME")

# Menyusun format URL Database berstandar SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Membuat Engine (Pusat pengelola koneksi database)
engine = create_engine(DATABASE_URL)

# Membuat Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# FUNGSI INI YANG SEBELUMNYA HILANG DAN DIBUTUHKAN OLEH FASTAPI (ml.py)
def get_db():
    """
    Dependency Injection untuk FastAPI.
    Fungsi ini akan membuka sesi, memberikannya ke Service, 
    dan OTOMATIS menutupnya (db.close) saat proses selesai atau terjadi error.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()