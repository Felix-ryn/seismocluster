from app.config.database import get_cursor

conn, cursor = get_cursor()

cursor.execute("SELECT current_database();")
print(cursor.fetchone())