import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

from database import create_db, add_user, validate_user
from utils import generate_complaint_id, detect_priority, detect_jurisdiction
from mlat_generator import generate_mlat_pdf

# ---------------- UI ----------------
st.set_page_config(page_title="C3IS System", layout="wide")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(120deg, #0f2027, #203a43, #2c5364);
    color: white;
}
</style>
""", unsafe_allow_html=True)

create_db()

if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None

# ---------------- LOGIN ----------------
def login():
    st.title("🔐 C3IS LOGIN")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])

    if st.button("Login"):
        user = validate_user(u, p)
        if user:
            st.session_state.user = u
            st.session_state.role = role
            st.success("Logged in")
            st.rerun()

    if st.button("Register"):
        add_user(u, p, role)
        st.success("Registered")

# ---------------- USER ----------------
def user_panel():
    st.header("📢 Submit Cyber Crime Complaint")

    title = st.text_input("Title")
    desc = st.text_area("Description")

    location = st.text_input("Location")
    fraud_type = st.selectbox("Fraud Type", [
        "UPI Fraud",
        "OTP Fraud",
        "Banking Fraud",
        "Crypto Scam",
        "Fake Job Scam"
    ])

    if st.button("Submit"):
        complaint_id = generate_complaint_id()
        priority = detect_priority(fraud_type)
        jurisdiction = detect_jurisdiction(desc)

        conn = sqlite3.connect("complaints.db")
        c = conn.cursor()

        c.execute('''INSERT INTO complaints
        (complaint_id, username, title, description, location, fraud_type, priority, jurisdiction)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
        (complaint_id, st.session_state.user, title, desc, location, fraud_type, priority, jurisdiction))

        conn.commit()
        conn.close()

        st.success(f"Complaint Submitted: {complaint_id}")

# ---------------- ADMIN ----------------
def admin_panel():
    st.header("🛡 C3IS Intelligence Dashboard")

    conn = sqlite3.connect("complaints.db")
    df = pd.read_sql_query("SELECT * FROM complaints", conn)

    st.metric("Total Cases", len(df))
    st.metric("High Risk Cases", len(df[df["priority"] == "HIGH"]))
    st.metric("International Cases", len(df[df["jurisdiction"].str.contains("INTERNATIONAL")]))

    st.subheader("Fraud Analytics")
    st.plotly_chart(px.histogram(df, x="fraud_type", color="priority"))

    st.subheader("Location Analysis")
    st.plotly_chart(px.bar(df, x="location", color="fraud_type"))

    st.subheader("Jurisdiction Split")
    st.plotly_chart(px.pie(df, names="jurisdiction"))

    st.subheader("⚠ Case Management")

    cid = st.text_input("Complaint ID")
    status = st.selectbox("Update Status", ["Pending", "Under Investigation", "Resolved"])

    if st.button("Update"):
        c = conn.cursor()
        c.execute("UPDATE complaints SET status=? WHERE complaint_id=?", (status, cid))
        conn.commit()
        st.success("Updated")

    st.subheader("📄 MLAT Generator (International Cases)")

    if st.button("Generate MLAT Report"):
        if not df.empty:
            case = df.iloc[0].to_dict()
            file = generate_mlat_pdf(case)
            st.success(f"MLAT Report Generated: {file}")

# ---------------- ROUTER ----------------
if st.session_state.user is None:
    login()
else:
    st.sidebar.write(f"User: {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    if st.session_state.role == "user":
        user_panel()
    else:
        admin_panel()
