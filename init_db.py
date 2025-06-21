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
            username text not null,
            description TEXT)''')
    conn.commit()
    conn.close()
    print("table created")

createTable()

def show_data():
    query = 'select * from notes_table'
    conn = get_connection()
    c = conn.cursor()
    notes = c.execute(query).fetchall()
    
    for i in notes:
        print(i)
    
    
# show_data()


# def delete_all_row():
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute('DELETE FROM notes_table')
#     conn.commit()
#     conn.close()
#     print("deleted")

# delete_all_row()

# def drop_table():
#     conn = get_connection()
#     c = conn.cursor()
#     c.execute('drop table notes_table')
#     print(" table deleted")
# drop_table()