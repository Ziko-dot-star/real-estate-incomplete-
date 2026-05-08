import sqlite3
import os

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
    ''')
    
    # Staff table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS staff (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT DEFAULT 'Active',
        joined_date TEXT NOT NULL,
        image_url TEXT DEFAULT 'images/temp.jpg'
    )
    ''')
    
    # Properties table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS properties (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        location TEXT NOT NULL,
        price TEXT NOT NULL,
        description TEXT,
        status TEXT DEFAULT 'Available',
        image_url TEXT NOT NULL
    )
    ''')
    
    # Insert default admin if not exists
    cursor.execute("SELECT * FROM users WHERE email='admin@wisdomshelter.com'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (fullname, email, password, role) VALUES (?, ?, ?, ?)",
                       ('Super Admin', 'admin@wisdomshelter.com', 'admin123', 'admin'))
    
    # Insert some initial staff if table is empty
    cursor.execute("SELECT COUNT(*) FROM staff")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO staff (name, role, joined_date) VALUES (?, ?, ?)", 
                       ('John Doe', 'Real Estate Agent', 'Jan 12, 2024'))
        cursor.execute("INSERT INTO staff (name, role, joined_date) VALUES (?, ?, ?)", 
                       ('Jane Smith', 'Property Manager', 'Feb 05, 2024'))

    # Insert initial properties if empty
    cursor.execute("SELECT COUNT(*) FROM properties")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO properties (title, location, price, description, image_url) VALUES (?, ?, ?, ?, ?)",
                       ('Luxury Villa', 'Lekki, Lagos', '$5,000/mo', 'A beautiful 4-bedroom villa with modern amenities.', 'images/0b30aba482d289418f887076b8ecae94.jpg'))
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

if __name__ == '__main__':
    init_db()
