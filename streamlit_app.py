
import streamlit as st
import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill
from datetime import datetime
from io import BytesIO
import re

st.set_page_config(page_title="Daily Replenishment Generator", layout="wide")
st.title("📦 Daily Replenishment & Procurement Generator")

st.markdown("""
### Upload your data files below

**One-Time Uploads:**
- Overall Master.csv
- status.csv
- sales_file.csv (6-month sales, can be updated monthly)

**Daily Uploads:**
- Warehouse Stock CSV
- Store Stock CSV
""")

# File Uploads
master_file = st.file_uploader("🧾 Upload Overall Master.csv", type="csv")
status_file = st.file_uploader("📋 Upload status.csv", type="csv")
sales_file = st.file_uploader("📊 Upload 6-month sales_file.csv (Strips)", type="csv")
warehouse_file = st.file_uploader("🏬 Upload Warehouse Stock CSV (Loose Units)", type="csv")
store_file = st.file_uploader("🏪 Upload Store Stock CSV (Loose Units)", type="csv")

if master_file and status_file and sales_file and warehouse_file and store_file:
    master = pd.read_csv(master_file).iloc[:, :4]  # drop unnamed trailing columns
    status = pd.read_csv(status_file)
    sales = pd.read_csv(sales_file)
    warehouse = pd.read_csv(warehouse_file)
    store = pd.read_csv(store_file)

    master = master.merge(status, on="Item Code", how="left")
    master["Status"] = master["Status"].fillna("Active")

    # Sales Summary
    
# Use normalized matching key instead of direct merge
master["match_key"] = master["Medicines Name"].str.strip().str.lower() + "|" + master["Unit"].str.strip().str.lower()
sales["match_key"] = sales["Medicines Name"].str.strip().str.lower() + "|" + sales["Pack Size"].str.strip().str.lower()

sales_merged = sales.merge(master[["Item Code", "match_key"]], on="match_key", how="left")
    sales_merged = sales_merged.dropna(subset=["Item Code"])
    sales_summary = sales_merged.groupby("Item Code").agg({
        "Total Quantity(Strip)": "sum"
    }).reset_index()
    sales_summary["Weekly Sale"] = sales_summary["Total Quantity(Strip)"] / 24
    sales_summary["Min Stock"] = (sales_summary["Weekly Sale"] * 2).round().astype(int)
    sales_summary["Max Stock"] = (sales_summary["Weekly Sale"] * 4).round().astype(int)
    master = master.merge(sales_summary[["Item Code", "Min Stock", "Max Stock"]], on="Item Code", how="left")
    master["Min Stock"] = master["Min Stock"].fillna(0).astype(int)
    master["Max Stock"] = master["Max Stock"].fillna(0).astype(int)

    # Merge Current Stock
    data = master.merge(warehouse[["Item Code", "Stock"]].rename(columns={"Stock": "Warehouse Stock"}), on="Item Code", how="left")
    data = data.merge(store[["Item Code", "Stock"]].rename(columns={"Stock": "Store Stock"}), on="Item Code", how="left")
    data["Warehouse Stock"] = data["Warehouse Stock"].fillna(0)
    data["Store Stock"] = data["Store Stock"].fillna(0)

    # Convert loose units to strips
    def to_strips(row, column):
        unit = str(row["Unit"]).lower()
        val = row[column]
        if any(x in unit for x in ["ml", "ltr", "gm", "g", "l"]):
            return val
        match = re.search(r"(\d+)", unit)
        if match:
            divisor = int(match.group(1))
            return round(val / divisor, 2) if divisor else val
        return val

    data["Store Stock (Strips)"] = data.apply(lambda x: to_strips(x, "Store Stock"), axis=1)
    data["Warehouse Stock (Strips)"] = data.apply(lambda x: to_strips(x, "Warehouse Stock"), axis=1)

    # Replenishment and Procurement Logic
    def calc_replenishment(row):
        if row["Status"] == "Discontinued":
            return 0
        if row["Store Stock (Strips)"] < row["Min Stock"] and row["Warehouse Stock (Strips)"] > 0:
            return min(row["Max Stock"] - row["Store Stock (Strips)"], row["Warehouse Stock (Strips)"])
        return 0

    def calc_procurement(row):
        if row["Status"] == "Discontinued":
            return 0
        total = row["Store Stock (Strips)"] + row["Warehouse Stock (Strips)"]
        return max(row["Max Stock"] - total, 0) if total < row["Min Stock"] else 0

    data["Replenishment Qty"] = data.apply(calc_replenishment, axis=1)
    data["Procurement Qty"] = data.apply(calc_procurement, axis=1)

    today = datetime.today().strftime("%Y-%m-%d")
    rep = data[data["Replenishment Qty"] > 0]
    proc = data[data["Procurement Qty"] > 0]

    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return output.getvalue()

    st.success(f"✅ Generated successfully for {today}")
    st.download_button(f"⬇️ Download Replenishment List – {today}", to_excel(rep), file_name=f"Replenishment_List_{today}.xlsx")
    st.download_button(f"⬇️ Download Procurement List – {today}", to_excel(proc), file_name=f"Procurement_List_{today}.xlsx")

else:
    st.info("Upload all required files above to enable processing.")
