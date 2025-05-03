
import streamlit as st
import pandas as pd
import json
import os

def admin_page():
    st.title("🔐 Admin - Upload Master, Status, Sales")
    password = st.text_input("Enter Admin Password", type="password")
    if password != "Nemo_63":
        st.warning("Unauthorized access")
        return

    st.success("Access Granted ✅")

    master = st.file_uploader("Upload Master File", type="csv")
    status = st.file_uploader("Upload Status File", type="csv")
    sales = st.file_uploader("Upload 6-Month Sales File", type="csv")

    min_week = st.number_input("Min Weeks", min_value=1, max_value=4, value=2)
    max_week = st.number_input("Max Weeks", min_value=2, max_value=8, value=4)

    if st.button("Save Config"):
        with open("config.json", "w") as f:
            json.dump({"min_weeks": min_week, "max_weeks": max_week}, f)
        st.success("Config saved")

    if master:
        df = pd.read_csv(master)
        df.to_csv("Overall Master.csv", index=False)
        st.success("Master uploaded")

    if status:
        df = pd.read_csv(status)
        df.to_csv("Status.csv", index=False)
        st.success("Status uploaded")

    if sales:
        df = pd.read_csv(sales)
        df.to_csv("sales_file.csv", index=False)
        st.success("Sales uploaded")
