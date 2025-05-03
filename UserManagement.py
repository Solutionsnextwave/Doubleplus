import streamlit as st
import json
import os

st.set_page_config(page_title="User Management", layout="wide")

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("🔐 Access Denied. Please login first.")
    st.stop()

st.title("👤 User Management")

if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump([], f)

with open("users.json", "r") as f:
    users = json.load(f)

st.subheader("Create New User")
with st.form("create_user"):
    uname = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["View", "Edit", "Delete"])
    create = st.form_submit_button("Create User")
    if create:
        users.append({"username": uname, "password": pwd, "role": role})
        with open("users.json", "w") as f:
            json.dump(users, f)
        st.success(f"User {uname} created!")

st.subheader("📋 Existing Users")
for user in users:
    st.write(f"👤 {user['username']} - Role: {user['role']}")
