import sqlite3

def get_connection():
    conn =sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def createTable():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT)''')
    conn.commit()
    conn.close()
    print("db created")

createTable()