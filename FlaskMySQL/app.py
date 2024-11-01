from flask import Flask, redirect, url_for, render_template, request, g
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'samples'

# Function to get a database connection
def get_db_connection():
    if 'db_conn' not in g:
        try:
            g.db_conn = mysql.connector.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DB']
            )
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            g.db_conn = None
    return g.db_conn

@app.route('/')
def index():
    conn = get_db_connection()
    data = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        cursor.close()
    return render_template('index.html', data=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        firstName = request.get_json().get('firstName')
        lastName = request.get_json().get('lastName')
        email = request.get_json().get('email')
        password = request.get_json().get('confirmPassword')
        address = request.get_json().get('address')
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO users(firstname, lastname, email, password, address) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, ( firstName, lastName, email, password, address))
            conn.commit()
            cursor.close()
            
            response = {
                'msg' : 'Successfully inserted user'
            }
            return response, 200
    
    response = {
            'error' : 'Invalid'
        }
    return response, 400

@app.route('/update_user/<int:id>', methods=['PUT', 'POST'])
def update_user(id):
    conn = get_db_connection()
    if request.method == 'PUT':
        firstName = request.get_json().get('firstName')
        lastName = request.get_json().get('lastName')
        email = request.get_json().get('email')
        password = request.get_json().get('confirmPassword')
        address = request.get_json().get('address')
        if conn:
            cursor = conn.cursor()
            sql = "UPDATE users SET firstname = %s, lastname = %s, email = %s, password = %s, address = %s WHERE id = %s"
            cursor.execute(sql, ( firstName, lastName, email, password, address, id))
            conn.commit()
            cursor.close()
            response = {
                'msg' : 'Successfully Updated'
            }
            return response, 200
    response = {
            'msg' : 'Internal Server Error'
        }
    return response, 500

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
