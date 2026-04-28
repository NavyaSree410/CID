import sqlite3
import bcrypt

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
        complaint_id TEXT,
        username TEXT,
        title TEXT,
        description TEXT,
        location TEXT,
        fraud_type TEXT,
        priority TEXT,
        jurisdiction TEXT,
        status TEXT DEFAULT 'Pending'
    )''')

    conn.commit()
    conn.close()


def hash_password(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt())


def check_password(pw, hashed):
    return bcrypt.checkpw(pw.encode(), hashed)


def add_user(u, p, r):
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (u, hash_password(p), r))
    conn.commit()
    conn.close()


def validate_user(u, p):
    conn = sqlite3.connect("complaints.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (u,))
    user = c.fetchone()
    conn.close()

    if user and check_password(p, user[1]):
        return user
    return None
