import sqlite3

def get_connection():
    conn =sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    # Connect to the database (creates it if it doesn't exist)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fullname TEXT NOT NULL,
            email TEXT NOT NULL unique,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    print("Database initialized and table created (if not exists).")


init_db()

# def show_data():
#     query = 'select * from users'
#     conn = get_connection()
#     c = conn.cursor()
#     notes = c.execute(query).fetchall()
    
#     for row in notes:
#         print(dict(row))
    
# show_data()

# def delete_all_row():
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute('DELETE FROM users')
#     conn.commit()
#     conn.close()
#     print("deleted")

# delete_all_row()


# def drop_table():
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute('drop table users')
#     print(" table deleted")
# drop_table()
