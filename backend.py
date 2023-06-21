from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_connection = None


def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='ssa2023'
        )
        return connection
    except Error as e:
        print('Error connecting to the database:', e)
        return None


def create_incident_table():
    global db_connection

    try:
        cursor = db_connection.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS incidents (id INT AUTO_INCREMENT PRIMARY KEY, time TIMESTAMP, worn INT(1))')
        db_connection.commit()
    except Error as e:
        print('Error creating incidents table:', e)


@app.before_request
def before_request():
    global db_connection
    db_connection = connect_to_database()
    if db_connection:
        create_incident_table()


@app.route('/incident', methods=['POST'])
def add_incident():
    data = request.get_json()
    time = data.get('time')
    worn = data.get('worn')
    if time and worn is not None:
        try:
            worn = 1 if worn else 0
            cursor = db_connection.cursor()
            query = 'INSERT INTO incidents (time, worn) VALUES (STR_TO_DATE(%s, \'%Y-%m-%d %H:%i:%S\'), %s)'
            values = (time, worn)
            cursor.execute(query, values)
            db_connection.commit()
            return jsonify({'message': 'Incident added successfully'}), 201
        except Error as e:
            print('Error adding incident:', e)
            return jsonify({'error': 'Failed to add incident'}), 500
    else:
        return jsonify({'error': 'Both time and worn fields are required'}), 400


@app.route('/incident', methods=['GET'])
def get_incidents():
    global db_connection
    try:
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute('SELECT * FROM incidents')
        incidents = cursor.fetchall()
        return jsonify(incidents), 200
    except Error as e:
        print('Error retrieving incidents:', e)
        return jsonify({'error': 'Failed to fetch incidents'}), 500


if __name__ == '__main__':
    app.run()