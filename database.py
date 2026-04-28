import sqlite3
import bcrypt

DB = "complaints.db"


# ---------------- DB INIT ----------------
def create_db():
    conn = sqlite3.connect(DB)
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


# ---------------- PASSWORD ----------------
def hash_password(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode("utf-8")


def check_password(pw, hashed):
    return bcrypt.checkpw(pw.encode(), hashed.encode("utf-8"))


# ---------------- USER SYSTEM (FIXED) ----------------
def add_user(username, password, role):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    try:
        c.execute("INSERT INTO users VALUES (?, ?, ?)",
                  (username, hash_password(password), role))
        conn.commit()
        return "SUCCESS"

    except sqlite3.IntegrityError:
        return "USER_EXISTS"

    finally:
        conn.close()


def validate_user(username, password):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()

    if user and check_password(password, user[1]):
        return user

    return None
