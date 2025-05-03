import streamlit as st
from pathlib import Path
import json

st.set_page_config(page_title="Double Plus Pharmacy", layout="wide")

def authenticate(username, password):
    with open("users.json", "r") as f:
        users = json.load(f)
    return username in users and users[username]["password"] == password

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Double Plus Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in successfully!")
            st.rerun()

        else:
            st.error("Invalid credentials")
else:
    st.sidebar.success(f"Logged in as {st.session_state.username}")
    st.title("🏥 Welcome to Double Plus Pharmacy Dashboard")
    st.write("Use the menu on the left to navigate.")
