from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DATABASE = 'database.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    fullname = data.get('fullname')
    email = data.get('email')
    password = data.get('password')
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (fullname, email, password) VALUES (?, ?, ?)',
                     (fullname, email, password))
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already exists"}), 400
    finally:
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password)).fetchone()
    conn.close()
    
    if user:
        return jsonify({
            "id": user['id'],
            "fullname": user['fullname'],
            "email": user['email'],
            "role": user['role']
        }), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/staff', methods=['GET'])
def get_staff():
    conn = get_db_connection()
    staff_list = conn.execute('SELECT * FROM staff').fetchall()
    conn.close()
    return jsonify([dict(row) for row in staff_list])

@app.route('/api/staff', methods=['POST'])
def add_staff():
    data = request.json
    name = data.get('name')
    role = data.get('role')
    joined_date = data.get('joined_date')
    
    conn = get_db_connection()
    conn.execute('INSERT INTO staff (name, role, joined_date) VALUES (?, ?, ?)',
                 (name, role, joined_date))
    conn.commit()
    conn.close()
    return jsonify({"message": "Staff added successfully"}), 201

@app.route('/api/staff/<int:id>', methods=['DELETE'])
def delete_staff(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM staff WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Staff removed successfully"})

@app.route('/api/properties', methods=['GET'])
def get_properties():
    conn = get_db_connection()
    properties = conn.execute('SELECT * FROM properties').fetchall()
    conn.close()
    return jsonify([dict(row) for row in properties])

if __name__ == '__main__':
    # Ensure database is initialized
    if not os.path.exists(DATABASE):
        from db_init import init_db
        init_db()
    app.run(debug=True, port=5000)
