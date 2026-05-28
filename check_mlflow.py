import sqlite3

conn = sqlite3.connect('backend/mlflow.db')
c = conn.cursor()

print('=== TABLES ===')
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(c.fetchall())

print()
print('=== REGISTERED MODELS ===')
try:
    c.execute('SELECT name FROM registered_models')
    print(c.fetchall())
except Exception as e:
    print('Error:', e)

print()
print('=== ALIASES (champion) ===')
try:
    c.execute("SELECT name, alias, version FROM registered_model_aliases WHERE alias='champion'")
    print(c.fetchall())
except Exception as e:
    print('Error:', e)

conn.close()