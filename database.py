import sqlite3
import bcrypt

DB = "complaints.db"


def create_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS complaints (
        complaint_id TEXT PRIMARY KEY,
        username TEXT,
        title TEXT,
        description TEXT,
        location TEXT,
        fraud_type TEXT,
        priority TEXT,
        timestamp TEXT
    )''')

    conn.commit()
    conn.close()


# ---------------- AUTH FIXED ----------------
def add_user(u, p, r):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    try:
        hashed = bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()
        c.execute("INSERT INTO users VALUES (?, ?, ?)", (u, hashed, r))
        conn.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conn.close()


def validate_user(u, p):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (u,))
    user = c.fetchone()

    conn.close()

    if user and bcrypt.checkpw(p.encode(), user[1].encode()):
        return user

    return None
