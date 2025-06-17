from flask import Flask,url_for,redirect,render_template,request
import sqlite3

app = Flask(__name__)
app.secret_key ="bharat@123"
def get_connection():
    conn =sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    conn = get_connection()
    cursor = conn.cursor()
    query ='select * from notes_table'
    cursor.execute(query)
    notes = cursor.fetchall()
    conn.close()
    return render_template('index.html',notes =notes)
@app.route('/add', methods =['POST'])
def add():
    title = request.form['title']
    notes = request.form['description']
    query = 'insert into notes_table(title,description) values(?,?)'
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query,(title,notes))
    conn.commit()
    conn.close()
    print("notes added")
    return redirect(url_for('index'))
@app.route('/delete/<int:id>')
def delete(id):
    query = 'delete from notes_table where id =?'
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query,(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    title = request.form['title']
    description = request.form['description']
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE notes_table SET title = ?, description = ? WHERE id = ?', (title, description, id))
    conn.commit()
    conn.close()
    
    return "Success", 200  # Return success response for JavaScript

if __name__ == '__main__':
    app.run(debug= True)
