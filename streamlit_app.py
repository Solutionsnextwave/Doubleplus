
import streamlit as st
import pandas as pd
import re
import os
import json
from datetime import datetime
from io import BytesIO

st.set_page_config(page_title="Double Plus | Replenishment", layout="wide")
st.markdown("<style>div.stButton > button {background-color:#0071BC; color:white;}</style>", unsafe_allow_html=True)

st.image("Double Plus Logo.png", width=180)
st.title("🧮 Daily Replenishment & Procurement Generator")
st.markdown("Min = 2 weeks, Max = 4 weeks (configurable in Admin)")
st.markdown("---")

st.header("📤 Upload Daily Stock Files")
store_file = st.file_uploader("🏪 Upload Store Stock CSV", type="csv")
warehouse_file = st.file_uploader("🏬 Upload Warehouse Stock CSV", type="csv")

if store_file and warehouse_file:
    st.success("✅ Files uploaded successfully")
    if st.button("⚙️ Generate Replenishment & Procurement"):
        try:
            # Load base files
            master = pd.read_csv("Overall Master.csv", low_memory=False).dropna(axis=1, how="all")
            status = pd.read_csv("Status.csv", low_memory=False).dropna(axis=1, how="all")
            sales = pd.read_csv("sales_file.csv", low_memory=False)

            config = {"min_weeks": 2, "max_weeks": 4}
            if os.path.exists("config.json"):
                with open("config.json", "r") as f:
                    config = json.load(f)

            # Clean and prepare
            master = master.loc[:, ~master.columns.str.contains("^Unnamed")]
            status = status.loc[:, ~status.columns.str.contains("^Unnamed")]

            # Merge Status
            master = master.merge(status[["Item Code", "Status"]], on="Item Code", how="left")
            master["Status"] = master["Status"].fillna("Active")

            # Build match keys
            master["match_key"] = master["Medicines Name"].str.strip().str.lower() + "|" + master["Unit"].str.strip().str.lower()
            sales["match_key"] = sales["Medicines Name"].str.strip().str.lower() + "|" + sales["Pack Size"].str.strip().str.lower()

            merged = sales.merge(master[["Item Code", "match_key"]], on="match_key", how="left").dropna(subset=["Item Code"])
            summary = merged.groupby("Item Code").agg({"Total Quantity(Strip)": "sum"}).reset_index()
            summary["Weekly Sale"] = summary["Total Quantity(Strip)"] / 24
            summary["Min Stock"] = (summary["Weekly Sale"] * config["min_weeks"]).round().astype(int)
            summary["Max Stock"] = (summary["Weekly Sale"] * config["max_weeks"]).round().astype(int)

            master = master.merge(summary[["Item Code", "Min Stock", "Max Stock"]], on="Item Code", how="left")
            master["Min Stock"] = master["Min Stock"].fillna(0).astype(int)
            master["Max Stock"] = master["Max Stock"].fillna(0).astype(int)

            # Read uploaded stocks
            store = pd.read_csv(store_file, low_memory=False)
            warehouse = pd.read_csv(warehouse_file, low_memory=False)

            # Merge stock
            df = master.merge(warehouse[["Item Code", "Stock"]].rename(columns={"Stock": "Warehouse Stock"}), on="Item Code", how="left")
            df = df.merge(store[["Item Code", "Stock"]].rename(columns={"Stock": "Store Stock"}), on="Item Code", how="left")
            df["Warehouse Stock"] = df["Warehouse Stock"].fillna(0)
            df["Store Stock"] = df["Store Stock"].fillna(0)

            # Convert to strips
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

            df["Store Stock (Strips)"] = df.apply(lambda x: to_strips(x, "Store Stock"), axis=1)
            df["Warehouse Stock (Strips)"] = df.apply(lambda x: to_strips(x, "Warehouse Stock"), axis=1)

            # Logic
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

            df["Replenishment Qty"] = df.apply(calc_replenishment, axis=1)
            df["Procurement Qty"] = df.apply(calc_procurement, axis=1)

            today = datetime.today().strftime("%Y-%m-%d")

            export_cols = ["Item Code", "Medicines Name", "Unit", "Min Stock", "Max Stock"]

            rep = df[df["Replenishment Qty"] > 0][export_cols + ["Replenishment Qty"]]
            rep = rep.rename(columns={"Unit": "Pack Size", "Replenishment Qty": "Qty"})

            proc = df[df["Procurement Qty"] > 0][export_cols + ["Procurement Qty"]]
            proc = proc.rename(columns={"Unit": "Pack Size", "Procurement Qty": "Qty"})

            def to_excel(dataframe):
                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                    dataframe.to_excel(writer, index=False)
                return buffer.getvalue()

            st.download_button("⬇️ Download Replenishment", data=to_excel(rep), file_name=f"Replenishment_List_{today}.xlsx")
            st.download_button("⬇️ Download Procurement", data=to_excel(proc), file_name=f"Procurement_List_{today}.xlsx")

        except Exception as e:
            st.error(f"⚠️ Error: {e}")
else:
    st.info("Please upload both store and warehouse stock files to begin.")
