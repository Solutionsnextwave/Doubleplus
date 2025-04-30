
import streamlit as st
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Double Plus | Replenishment", layout="wide")

# Logo Header
st.image("Double Plus Logo.png", width=180)
st.title("🧮 Replenishment & Procurement Generator")
st.markdown("Min Stock = 2 Weeks of Sales | Max Stock = 4 Weeks of Sales")
st.markdown("---")

# File uploads for daily use
st.header("📤 Upload Daily Stock Files")
store_file = st.file_uploader("📦 Upload Store Stock CSV (Loose Units)", type="csv", key="store")
warehouse_file = st.file_uploader("🏬 Upload Warehouse Stock CSV (Loose Units)", type="csv", key="warehouse")

# Only shows processing button if both files present
if store_file and warehouse_file:
    st.success("✅ Files uploaded successfully. Click below to generate output.")
    if st.button("⚙️ Generate Replenishment & Procurement Files"):
        st.info("This version does not include logic – only UI layout shown here.")
else:
    st.warning("Please upload both store and warehouse stock files to continue.")
