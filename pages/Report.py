
import streamlit as st
import pandas as pd
import re
import json
from datetime import datetime
from io import BytesIO

def report_page():
    st.title("📦 Replenishment Generator")
    store = st.file_uploader("Upload Store Stock", type="csv")
    warehouse = st.file_uploader("Upload Warehouse Stock", type="csv")
    if not (store and warehouse):
        return

    try:
        master = pd.read_csv("Overall Master.csv").dropna(axis=1, how="all")
        status = pd.read_csv("Status.csv").dropna(axis=1, how="all")
        sales = pd.read_csv("sales_file.csv")

        with open("config.json", "r") as f:
            config = json.load(f)

        master = master.merge(status[["Item Code", "Status"]], on="Item Code", how="left")
        master["Status"] = master["Status"].fillna("Active")
        master["match_key"] = master["Medicines Name"].str.lower().str.strip() + "|" + master["Unit"].str.lower().str.strip()
        sales["match_key"] = sales["Medicines Name"].str.lower().str.strip() + "|" + sales["Pack Size"].str.lower().str.strip()
        merged = sales.merge(master[["Item Code", "match_key"]], on="match_key", how="left").dropna(subset=["Item Code"])
        summary = merged.groupby("Item Code").agg({"Total Quantity(Strip)": "sum"}).reset_index()
        summary["Weekly Sale"] = summary["Total Quantity(Strip)"] / 24
        summary["Min Stock"] = (summary["Weekly Sale"] * config["min_weeks"]).round().astype(int)
        summary["Max Stock"] = (summary["Weekly Sale"] * config["max_weeks"]).round().astype(int)
        master = master.merge(summary[["Item Code", "Min Stock", "Max Stock"]], on="Item Code", how="left")
        master["Min Stock"] = master["Min Stock"].fillna(0).astype(int)
        master["Max Stock"] = master["Max Stock"].fillna(0).astype(int)

        store = pd.read_csv(store)
        warehouse = pd.read_csv(warehouse)
        df = master.merge(warehouse[["Item Code", "Stock"]].rename(columns={"Stock": "Warehouse Stock"}), on="Item Code", how="left")
        df = df.merge(store[["Item Code", "Stock"]].rename(columns={"Stock": "Store Stock"}), on="Item Code", how="left")
        df.fillna(0, inplace=True)

        def to_strips(row, column):
            unit = str(row["Unit"]).lower()
            val = row[column]
            if any(x in unit for x in ["ml", "ltr", "gm", "g", "l"]):
                return val
            match = re.search(r"(\d+)", unit)
            if match:
                return round(val / int(match.group(1)), 2)
            return val

        df["Store Strips"] = df.apply(lambda x: to_strips(x, "Store Stock"), axis=1)
        df["Warehouse Strips"] = df.apply(lambda x: to_strips(x, "Warehouse Stock"), axis=1)

        df["Replenishment Qty"] = df.apply(lambda x: min(x["Max Stock"] - x["Store Strips"], x["Warehouse Strips"]) if x["Status"] == "Active" and x["Store Strips"] <= x["Min Stock"] else 0, axis=1)
        df["Procurement Qty"] = df.apply(lambda x: max(x["Max Stock"] - (x["Store Strips"] + x["Warehouse Strips"]), 0) if x["Status"] == "Active" and (x["Store Strips"] + x["Warehouse Strips"]) < x["Min Stock"] else 0, axis=1)

        today = datetime.today().strftime("%Y-%m-%d")
        cols = ["Item Code", "Medicines Name", "Manufacturer/Company", "Unit"]
        rep = df[df["Replenishment Qty"] > 0][cols + ["Replenishment Qty"]].rename(columns={"Replenishment Qty": "Qty", "Unit": "Pack Size"})
        proc = df[df["Procurement Qty"] > 0][cols + ["Procurement Qty"]].rename(columns={"Procurement Qty": "Qty", "Unit": "Pack Size"})

        def to_excel(data):
            buffer = BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                data.to_excel(writer, index=False)
            return buffer.getvalue()

        st.download_button("Download Replenishment", data=to_excel(rep), file_name=f"Replenishment_List_{today}.xlsx")
        st.download_button("Download Procurement", data=to_excel(proc), file_name=f"Procurement_List_{today}.xlsx")
    except Exception as e:
        st.error(f"Error: {e}")
