import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

from database import create_db, add_user, validate_user
from utils import generate_id, priority, find_similar
from blockchain import add_block
from mlat import generate_mlat


st.set_page_config(page_title="C3IS BLOCKCHAIN", layout="wide")

# 🔥 HACKER UI
st.markdown("""
<style>
.stApp {
    background: black;
    color: #00ff88;
    font-family: monospace;
}

h1, h2, h3 {
    color: #00ff88;
}

.stButton>button {
    background: #00ff88;
    color: black;
    font-weight: bold;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

create_db()


if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- AUTH ----------------
def auth():
    st.title("⚡ C3IS BLOCKCHAIN SYSTEM")

    mode = st.radio("Mode", ["LOGIN", "REGISTER"])

    u = st.text_input("USER ID")
    p = st.text_input("PASSWORD", type="password")
    r = st.selectbox("ROLE", ["user", "admin"])

    if mode == "REGISTER":
        if st.button("REGISTER"):
            if add_user(u, p, r):
                st.success("REGISTERED")
            else:
                st.error("USER ALREADY EXISTS")

    if mode == "LOGIN":
        if st.button("LOGIN"):
            user = validate_user(u, p)
            if user:
                st.session_state.user = u
                st.success("ACCESS GRANTED")
                st.rerun()
            else:
                st.error("ACCESS DENIED")


# ---------------- USER ----------------
def user_panel():
    st.header("📡 REPORT CYBER INCIDENT")

    title = st.text_input("TITLE")
    desc = st.text_area("DESCRIPTION")
    location = st.text_input("LOCATION")

    fraud = st.selectbox("TYPE", [
        "UPI Fraud", "OTP Fraud", "Banking Fraud",
        "Crypto Scam", "Fake Job Scam"
    ])

    if st.button("SUBMIT"):
        cid = generate_id()
        pr = priority(fraud)

        block_data = {
            "complaint_id": cid,
            "user": st.session_state.user,
            "desc": desc,
            "time": str(datetime.now())
        }

        add_block(block_data)

        conn = sqlite3.connect("complaints.db")
        c = conn.cursor()

        c.execute('''INSERT INTO complaints VALUES (?,?,?,?,?,?,?,?)''',
                  (cid, st.session_state.user, title, desc, location, fraud, pr, str(datetime.now())))

        conn.commit()
        conn.close()

        st.success(f"LOGGED IN BLOCKCHAIN: {cid}")


# ---------------- ADMIN ----------------
def admin_panel():
    st.header("🧠 INTELLIGENCE DASHBOARD")

    conn = sqlite3.connect("complaints.db")
    df = pd.read_sql_query("SELECT * FROM complaints", conn)

    st.metric("TOTAL CASES", len(df))

    st.dataframe(df)

    st.subheader("FRAUD ANALYTICS")
    st.bar_chart(df["fraud_type"].value_counts())

    if st.button("GENERATE MLAT"):
        file = generate_mlat(df.iloc[0].to_dict())
        st.success(file)


# ---------------- ROUTER ----------------
if st.session_state.user is None:
    auth()
else:
    st.sidebar.write(f"USER: {st.session_state.user}")

    if st.sidebar.button("LOGOUT"):
        st.session_state.user = None
        st.rerun()

    user_panel() if st.session_state.user != "admin" else admin_panel()
