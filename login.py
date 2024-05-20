from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Function to establish connection to MySQL database
def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="chatbot"
    )

# Route to handle login page
@app.route('/login')
def login_page():
     return render_template('login.html')

# Route to handle form submission

@app.route('/login', methods =['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Connect to the database
    connection = connect_to_database()
    cursor = connection.cursor()

    # Execute a query to check if user exists with provided credentials
    query = "SELECT * FROM admin WHERE username=%s AND password=%s"
    cursor.execute(query, (username, password))
    user = cursor.fetchone()

    # Close cursor and connection
    cursor.close()
    connection.close()

    if user:
        # Successful login, redirect to dashboard or home page
        # return redirect(url_for('dashboard'))
        return render_template('dashboard.html')
    else:
        # Invalid credentials, redirect back to login page
        msg = 'Incorrect username / password !'
        return render_template('login.html',msg=msg)
        

# Route to handle dashboard page
# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')


