import streamlit as st
import pandas as pd
import plotly.express as px

from db import init_db, insert_case, fetch_cases, get_case
from auth import login, register
from ml_engine import detect_jurisdiction
from alert import trigger_alert, alerts
from blockchain import add_block
from mlat import generate
from utils import generate_case_id


st.set_page_config("C3IS MLAT SYSTEM", layout="wide")

init_db()

if "user" not in st.session_state:
    st.session_state.user = None


# ---------------- AUTH ----------------
def auth():
    st.title("🛡 C3IS MLAT SYSTEM")

    mode = st.radio("Mode", ["LOGIN", "REGISTER"])

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    r = st.selectbox("Role", ["user", "admin"])

    if mode == "REGISTER":
        if st.button("Register"):
            if register(u, p, r):
                st.success("Registered")
            else:
                st.error("Failed")

    if mode == "LOGIN":
        if st.button("Login"):
            if login(u, p):
                st.session_state.user = u
                st.rerun()
            else:
                st.error("Invalid login")


# ---------------- USER ----------------
def user():
    st.header("📥 Report Cybercrime")

    title = st.text_input("Title")
    desc = st.text_area("Description")
    location = st.text_input("Location")

    fraud = st.selectbox("Fraud Type", ["OTP Fraud", "Banking Fraud", "Crypto Scam"])

    if st.button("Submit Case"):
        cid = generate_case_id()

        jurisdiction = detect_jurisdiction(desc)

        police = "Cyber Cell HQ"

        if "INTERNATIONAL" in jurisdiction:
            trigger_alert(cid, location, police)

        data = (cid, st.session_state.user, title, desc, location, fraud, jurisdiction, str(pd.Timestamp.now()))

        insert_case(data)

        add_block({"case": cid, "desc": desc})

        st.success(f"Case Created: {cid}")


# ---------------- ADMIN ----------------
def admin():
    st.header("🧠 MLAT INTELLIGENCE DASHBOARD")

    data = fetch_cases()
    df = pd.DataFrame(data, columns=[
        "case_id","user","title","desc","location","fraud","jurisdiction","time"
    ])

    st.metric("Total Cases", len(df))

    st.subheader("Cases")
    st.dataframe(df)

    st.subheader("Fraud Graph")
    st.bar_chart(df["fraud"].value_counts())

    st.subheader("Jurisdiction Graph")
    st.bar_chart(df["jurisdiction"].value_counts())

    st.subheader("🚨 ACTIVE MLAT ALERTS")
    st.write(alerts)

    st.subheader("🔎 Search Case")

    cid = st.text_input("Case ID")

    if st.button("Search"):
        res = get_case(cid)
        st.write(res)

    st.subheader("📄 MLAT Report")

    if st.button("Generate Report"):
        if len(df) > 0:
            file = generate(df.iloc[-1])
            st.success(file)


# ---------------- ROUTER ----------------
if st.session_state.user is None:
    auth()
else:
    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.rerun()

    user() if st.session_state.user != "admin" else admin()
