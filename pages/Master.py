
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

st.set_page_config(page_title="Double Plus | Master Editor", layout="wide")
st.title("📘 Master Data Editor")
PASSWORD = "Nemo_63"

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    password = st.text_input("Enter Password", type="password")
    if password == PASSWORD:
        st.session_state["authenticated"] = True
        st.experimental_rerun()
    else:
        st.stop()

st.markdown("Edit `Status` or `Unit` directly. Click 'Save Changes' to update the Master.")

master = pd.read_csv("Overall Master.csv")
status_df = pd.read_csv("Status.csv")
df = master.merge(status_df[["Item Code", "Status"]], on="Item Code", how="left")
df["Status"] = df["Status"].fillna("Active")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_columns(["Item Code", "Medicines Name", "Unit", "Status"], editable=True)
gb.configure_pagination()
grid = AgGrid(df, gridOptions=gb.build(), update_mode=GridUpdateMode.MANUAL)

if st.button("💾 Save Changes"):
    updated = grid["data"]
    updated.to_csv("Overall Master.csv", index=False)
    updated[["Item Code", "Status"]].to_csv("Status.csv", index=False)
    st.success("✅ Master updated successfully!")
