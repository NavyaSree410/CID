import streamlit as st
import pandas as pd
from datetime import datetime

from db import init_db, insert_case, fetch_cases, get_case
from auth import login, register
from ml_engine import detect_jurisdiction
from alert import trigger_alert, alerts
from blockchain import add_block
from utils import generate_case_id

st.set_page_config("MLAT SYSTEM", layout="wide")

init_db()

if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- AUTH ----------------
def auth():
    st.title("🛡 MLAT SYSTEM")

    mode = st.radio("Mode", ["LOGIN", "REGISTER"])

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if mode == "REGISTER":
        if st.button("Register"):
            if register(u, p):
                st.success("Registered")
            else:
                st.error("User exists")

    if mode == "LOGIN":
        if st.button("Login"):
            if login(u, p):
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid login")


# ---------------- USER ----------------
def user():
    st.header("📥 Submit Case")

    title = st.text_input("Title")
    desc = st.text_area("Description")
    location = st.text_input("Location")

    fraud = st.selectbox("Fraud Type", ["OTP", "Bank", "Crypto"])

    if st.button("Submit Case"):
        cid = generate_case_id()

        jurisdiction = detect_jurisdiction(desc)

        # ✅ SHOW MLAT RESULT (IMPORTANT FIX)
        st.info(f"🧠 MLAT RESULT: {jurisdiction}")

        if "INTERNATIONAL" in jurisdiction:
            trigger_alert(cid, location)
            st.warning("🚨 ALERT TRIGGERED")

        data = (
            cid,
            st.session_state.user,
            title,
            desc,
            location,
            fraud,
            jurisdiction,
            str(datetime.now())
        )

        insert_case(data)
        add_block(data)

        st.success(f"Case Created: {cid}")


# ---------------- ADMIN ----------------
def admin():
    st.header("📊 DASHBOARD")

    df = pd.DataFrame(fetch_cases(), columns=[
        "case_id","user","title","desc","location",
        "fraud","jurisdiction","time"
    ])

    st.metric("Total Cases", len(df))

    st.dataframe(df)

    st.subheader("Fraud Graph")
    st.bar_chart(df["fraud"].value_counts())

    st.subheader("Location Graph")
    st.bar_chart(df["location"].value_counts())

    st.subheader("Jurisdiction Graph")
    st.bar_chart(df["jurisdiction"].value_counts())

    st.subheader("🚨 Alerts")
    st.write(alerts)

    st.subheader("🔎 Search Case")

    cid = st.text_input("Enter Case ID")

    if st.button("Search"):
        st.write(get_case(cid))


# ---------------- ROUTER ----------------
if st.session_state.user is None:
    auth()
else:
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    user() if st.session_state.user != "admin" else admin()
