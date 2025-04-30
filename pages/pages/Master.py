
import streamlit as st
import pandas as pd
import os

PASSWORD = "Nemo_63"
st.set_page_config(page_title="Master View - Double Plus", layout="wide")

if "auth_master" not in st.session_state:
    st.session_state["auth_master"] = False

if not st.session_state["auth_master"]:
    pwd = st.text_input("Enter master page password", type="password")
    if pwd == PASSWORD:
        st.session_state["auth_master"] = True
        st.experimental_rerun()
    else:
        st.stop()

st.title("📘 Master Management")

if not os.path.exists("Overall Master.csv"):
    st.warning("Please upload Master from Admin Page first.")
    st.stop()

df = pd.read_csv("Overall Master.csv")
search = st.text_input("🔍 Search Medicine or Item Code").lower()
if search:
    df = df[df["Medicines Name"].str.lower().str.contains(search) | df["Item Code"].str.lower().str.contains(search)]

edited = st.data_editor(df, num_rows="dynamic", use_container_width=True)
if st.button("💾 Save Changes to Master"):
    edited.to_csv("Overall Master.csv", index=False)
    st.success("✅ Saved updated master")
