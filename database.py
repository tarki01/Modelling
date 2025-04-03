import sqlite3

def get_db_connection():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    # Создаем таблицу, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT UNIQUE,
                      password TEXT,
                      csv_file BLOB)''')
    conn.commit()
    return conn, cursor
