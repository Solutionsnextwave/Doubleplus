
import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Double Plus Debug", layout="wide")

st.title("🧪 Debug: Check Uploaded File Columns")

store_file = st.file_uploader("Upload Store Stock", type="csv")
warehouse_file = st.file_uploader("Upload Warehouse Stock", type="csv")

st.subheader("Master, Status, and Sales Files (Pre-loaded)")
missing_files = []
for fname in ["Overall Master.csv", "Status.csv", "sales_file.csv"]:
    if not os.path.exists(fname):
        missing_files.append(fname)
if missing_files:
    st.error(f"Missing required files: {', '.join(missing_files)}")
else:
    try:
        master = pd.read_csv("Overall Master.csv", low_memory=False)
        status = pd.read_csv("Status.csv", low_memory=False)
        sales = pd.read_csv("sales_file.csv", low_memory=False)

        st.success("✅ Base files loaded successfully.")
        st.write("📋 **Master Columns**:", list(master.columns))
        st.write("📋 **Status Columns**:", list(status.columns))
        st.write("📋 **Sales Columns**:", list(sales.columns))

    except Exception as e:
        st.error(f"Error reading base files: {e}")

if store_file:
    try:
        store = pd.read_csv(store_file, low_memory=False)
        st.write("🏪 **Store Stock Columns**:", list(store.columns))
    except Exception as e:
        st.error(f"Error reading store stock: {e}")

if warehouse_file:
    try:
        warehouse = pd.read_csv(warehouse_file, low_memory=False)
        st.write("🏬 **Warehouse Stock Columns**:", list(warehouse.columns))
    except Exception as e:
        st.error(f"Error reading warehouse stock: {e}")
