import sqlite3

def create_db():
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        title TEXT,
        description TEXT,
        location TEXT,
        status TEXT DEFAULT 'Pending'
    )''')

    conn.commit()
    conn.close()


def add_user(username, password, role):
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (username, password, role))
    conn.commit()
    conn.close()


def validate_user(username, password):
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()


def add_complaint(username, title, description, location):
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("INSERT INTO complaints (username, title, description, location) VALUES (?, ?, ?, ?)",
              (username, title, description, location))
    conn.commit()
    conn.close()
