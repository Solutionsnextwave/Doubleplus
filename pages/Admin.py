
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime

PASSWORD = "Nemo_63"
st.set_page_config(page_title="Admin - Double Plus", layout="wide")

# Password protection
if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    pwd = st.text_input("Enter admin password", type="password")
    if pwd == PASSWORD:
        st.session_state["auth"] = True
        st.experimental_rerun()
    else:
        st.stop()

st.title("🔐 Admin Uploads & Configuration")

# Uploads
st.subheader("📂 Upload Core Files")

master_file = st.file_uploader("Upload Overall Master.csv", type="csv")
status_file = st.file_uploader("Upload Status.csv", type="csv")
sales_file = st.file_uploader("Upload 6 Month Sales.csv", type="csv")

if master_file:
    df = pd.read_csv(master_file)
    df.to_csv("Overall Master.csv", index=False)
    st.success("✅ Master uploaded")
    st.write(df.head())

if status_file:
    df = pd.read_csv(status_file)
    df.to_csv("Status.csv", index=False)
    st.success("✅ Status uploaded")

if sales_file:
    df = pd.read_csv(sales_file)
    df.to_csv("sales_file.csv", index=False)
    st.success("✅ Sales uploaded")

# Configurable Min/Max
st.markdown("---")
st.subheader("⚙️ Configure Min/Max Logic")

min_week = st.selectbox("Min Stock = X Weeks", [1, 2, 3], index=1)
max_week = st.selectbox("Max Stock = X Weeks", [2, 3, 4], index=2)

if st.button("💾 Save Configuration"):
    with open("config.json", "w") as f:
        json.dump({"min_weeks": min_week, "max_weeks": max_week}, f)
    st.success("✅ Config saved")

# Show last upload status
st.markdown("---")
st.subheader("📅 Last Uploaded File Info")
for filename in ["Overall Master.csv", "Status.csv", "sales_file.csv"]:
    if os.path.exists(filename):
        timestamp = datetime.fromtimestamp(os.path.getmtime(filename)).strftime("%Y-%m-%d %H:%M:%S")
        st.markdown(f"**{filename}**: {timestamp}")
    else:
        st.markdown(f"**{filename}**: ❌ Not uploaded yet")

# Download & reupload master
st.markdown("---")
st.subheader("📥 Download & Re-upload Master")
if os.path.exists("Overall Master.csv"):
    st.download_button("⬇️ Download Current Master", data=open("Overall Master.csv", "rb"), file_name="Master_Backup.csv")

reup_file = st.file_uploader("🔁 Re-upload Edited Master.csv", type="csv")
if reup_file:
    pd.read_csv(reup_file).to_csv("Overall Master.csv", index=False)
    st.success("✅ Re-uploaded master file successfully.")
