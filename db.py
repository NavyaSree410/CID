import sqlite3

DB = "cases.db"


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT,
        role TEXT
    )""")

    c.execute("""CREATE TABLE IF NOT EXISTS cases (
        case_id TEXT PRIMARY KEY,
        username TEXT,
        title TEXT,
        description TEXT,
        location TEXT,
        fraud_type TEXT,
        jurisdiction TEXT,
        timestamp TEXT
    )""")

    conn.commit()
    conn.close()


def insert_case(data):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("INSERT INTO cases VALUES (?,?,?,?,?,?,?,?)", data)

    conn.commit()
    conn.close()


def fetch_cases():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM cases")
    data = c.fetchall()

    conn.close()
    return data


def get_case(case_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("SELECT * FROM cases WHERE case_id=?", (case_id,))
    row = c.fetchone()

    conn.close()
    return row
