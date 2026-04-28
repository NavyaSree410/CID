import sqlite3
import bcrypt

DB_NAME = "complaints.db"


# ---------------- CREATE DB ----------------
def create_db():
    conn = sqlite3.connect(DB_NAME)
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


# ---------------- PASSWORD HASH ----------------
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")


def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode("utf-8"))


# ---------------- USER ----------------
def add_user(username, password, role):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)",
                  (username, hash_password(password), role))
        conn.commit()
    except:
        pass

    conn.close()


def validate_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password(password, user[1]):
        return user

    return None
