import sqlite3
import bcrypt

DB = "cases.db"


def register(u, p, r):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    try:
        hashed = bcrypt.hashpw(p.encode(), bcrypt.gensalt()).decode()
        c.execute("INSERT INTO users VALUES (?,?,?)", (u, hashed, r))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()


def login(u, p):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE username=?", (u,))
    user = c.fetchone()

    conn.close()

    if user and bcrypt.checkpw(p.encode(), user[1].encode()):
        return True

    return False
