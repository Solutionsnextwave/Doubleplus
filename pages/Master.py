
import streamlit as st
import pandas as pd
import os

PASSWORD = "Nemo_63"
st.set_page_config(page_title="Master View - Double Plus", layout="wide")

pwd = st.text_input("Enter master page password", type="password")
if pwd != PASSWORD:
    st.stop()

st.title("📘 Master Management")

if not os.path.exists("Overall Master.csv"):
    st.warning("Please upload Master from Admin Page first.")
    st.stop()

df = pd.read_csv("Overall Master.csv", low_memory=False)
search = st.text_input("🔍 Search by Medicine Name or Item Code").lower()

if search:
    df = df[df["Medicines Name"].str.lower().str.contains(search) | df["Item Code"].str.lower().str.contains(search)]

edited = st.data_editor(df, num_rows="dynamic", use_container_width=True, key="master_editor")

if st.button("💾 Save Changes to Master"):
    edited.to_csv("Overall Master.csv", index=False)
    st.success("✅ Changes saved to master")
