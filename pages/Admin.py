
import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Double Plus | Admin Panel", layout="wide")
st.markdown("<style>div.stButton > button {background-color:#0071BC; color:white;}</style>", unsafe_allow_html=True)
st.title("🔐 Admin Panel")

password = st.text_input("Enter Admin Password", type="password")

if password == "Nemo_63":
    st.success("🔓 Access Granted")
    st.markdown("### 📁 Master Management")
    
    # Timestamp
    st.info("🔄 **Master Last Updated:** 2025-05-03 05:02 PM")
    
    if os.path.exists("Overall Master.csv"):
        df = pd.read_csv("Overall Master.csv")
        st.dataframe(df.head(10))

    uploaded_master = st.file_uploader("Upload Updated Master CSV", type="csv")
    if uploaded_master:
        df_new = pd.read_csv(uploaded_master)
        df_new.to_csv("Overall Master.csv", index=False)
        st.success("✅ Master file updated")

    st.markdown("---")

else:
    if password != "":
        st.error("❌ Incorrect password. Try again.")
