import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
from database import create_db, add_user, validate_user, add_complaint

# ---------------- UI CONFIG ----------------
st.set_page_config(page_title="Cyber Crime Dashboard", layout="wide")

# Gradient UI
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
    color: white;
}
</style>
""", unsafe_allow_html=True)

create_db()

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None
    st.session_state.role = None


# ---------------- LOGIN ----------------
def login():
    st.title("🔐 Cyber Crime Portal Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    role = st.selectbox("Login As", ["user", "admin"])

    if st.button("Login"):
        user = validate_user(username, password)
        if user:
            st.session_state.user = username
            st.session_state.role = role
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("Register User"):
        add_user(username, password, role)
        st.success("User Registered")


# ---------------- USER PANEL ----------------
def user_panel():
    st.header("📢 Submit Cyber Crime Complaint")

    title = st.text_input("Complaint Title")
    desc = st.text_area("Description")
    location = st.text_input("Location (City)")

    if st.button("Submit Complaint"):
        add_complaint(st.session_state.user, title, desc, location)
        st.success("Complaint Submitted Successfully")

    st.subheader("Your Complaints")

    conn = sqlite3.connect("complaints.db")
    df = pd.read_sql_query(f"SELECT * FROM complaints WHERE username='{st.session_state.user}'", conn)
    st.dataframe(df)


# ---------------- ADMIN PANEL ----------------
def admin_panel():
    st.header("🛡 Admin Dashboard")

    conn = sqlite3.connect("complaints.db")
    df = pd.read_sql_query("SELECT * FROM complaints", conn)

    st.subheader("All Complaints")
    st.dataframe(df)

    st.subheader("📊 Fraud Cases by Location")

    if not df.empty:
        fig = px.bar(df, x="location", color="location", title="Fraud Hotspots")
        st.plotly_chart(fig)

        fig2 = px.pie(df, names="location", title="Location Distribution")
        st.plotly_chart(fig2)


# ---------------- MAIN ----------------
if st.session_state.user is None:
    login()
else:
    st.sidebar.write(f"Logged in as: {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.role = None
        st.rerun()

    if st.session_state.role == "user":
        user_panel()
    else:
        admin_panel()
