from flask import Flask,url_for,redirect,render_template,request,flash,session
import sqlite3
import smtplib
from email.message import EmailMessage
import random
import os

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD =os.getenv('EMAIL_PASSWORD')
db = os.getenv('DB')
app = Flask(__name__)
app.secret_key = os.getenv('secret_key')

# connection for database
def get_connection():
    conn =sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn
#opt generator
def generate_otp():
    otp = random.randint(1000, 9999)
    return str(otp)

# mail Sender
def send_email(to_email, subject, message_body):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(message_body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/index/<username>')
def index(username):
    if 'username' in session:
        conn = get_connection()
        cursor = conn.cursor()
        query ='select * from notes_table where username =?'
        cursor.execute(query,(username,))
        notes = cursor.fetchall()
        conn.close()
        return render_template('index.html',notes =notes,username=username)
    else:
        return redirect(url_for('login'))

@app.route('/add/<username>', methods =['POST'])
def add(username):
    if 'username' in session:
        title = request.form['title']
        notes = request.form['description']
        query = 'insert into notes_table(title,description,username) values(?,?,?)'
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query,(title,notes,username))
        conn.commit()
        conn.close()
        print("notes added")
        return redirect(url_for('index', username = username))
    else:
        return redirect(url_for('login'))

@app.route('/delete/<int:id>/<username>')
def delete(id,username):
    if 'username' in session:
        query = 'delete from notes_table where id =?'
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query,(id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index',username = username))
    else :
        return redirect(url_for('login'))

@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    if 'username' in session:
        title = request.form['title']
        description = request.form['description']
        
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE notes_table SET title = ?, description = ? WHERE id = ?', (title, description, id))
        conn.commit()
        conn.close()
        
        return "Success", 200  # Return success response for JavaScript
    else:
        return redirect(url_for('login'))

@app.route('/', methods =['POST','GET'])
def login():
    if request.method =="POST":
        username = request.form['username']
        password = request.form['password']
        query = 'select password from users where username =?'
        conn = get_connection()
        cursor = conn.cursor()
        result = cursor.execute(query, (username,)).fetchone()
        conn.close()

        if result is None:
            flash("Username not found!")
            return redirect(url_for('login'))
        elif result[0] != password:
            flash("Incorrect password!")
            return redirect(url_for('login'))
        else:
            session['username'] = username
            flash("Login successful!")
            return redirect(url_for('index', username = username))

    return render_template('login.html')

@app.route('/otp',methods=['POST','GET'])
def verify_otp():
    if request.method == 'POST':
        # entered_otp = request.form['otp']
        pending_user = session.get('pending_user')

        if not pending_user:
            flash("session expired")
            return redirect(url_for('register'))
    
        if int(request.form['otp']) == int(pending_user['otp']):
            conn = get_connection()
            cursor = conn.cursor()
            insert_query = 'insert into users(fullname,email,username,password) values(?,?,?,?)'
        
            cursor.execute(insert_query,(pending_user['fullname'],pending_user['email'],pending_user['username'],pending_user['password']))
            conn.commit()
            conn.close()
            session.pop('pending_user',None)
            flash("Congrats!!! you have registered")

            return redirect(url_for('login'))
        else:
            flash("incorrect otp")
            return redirect(url_for('verify_otp'))
        
    return render_template('otp.html')

@app.route('/register', methods =['POST','GET'])
def register():
    if request.method =="POST":
        fullname = request.form['fullname']
        password = request.form['password']
        email = request.form['email']
        username = request.form['username']
        
        conn = get_connection()
        cursor = conn.cursor()

        # 1. Check if username already exists
        check_username = "SELECT * FROM users WHERE username = ?"
        check_email = "SELECT * FROM users WHERE email = ?"
        cursor.execute(check_username, (username,))
        username_exist = cursor.fetchone()
        cursor.execute(check_email,(email,))
        email_exist = cursor.fetchone()
        conn.close()
        otp = generate_otp()
        
        # Store user data in session for later use
        session['pending_user'] = {
            'fullname': fullname,
            'email': email,
            'username': username,
            'password': password,
            'otp': otp
        }

        if username_exist :
            flash("Username already exists! go to login page.")
            return redirect(url_for('login'))
        elif email_exist :
            flash("email already exists! go to login page.")
            return redirect(url_for('login'))
        else:
            send_email(email,"otp verification",otp)
            flash("otp sent to your email")
            return redirect(url_for('verify_otp'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug= True)
