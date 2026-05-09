# filepath: backend/app/config/database.py
import os
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
import psycopg2

# Memuat variabel dari file .env
load_dotenv()

def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

def get_cursor():
    conn = get_connection()
    return conn, conn.cursor(cursor_factory=RealDictCursor)