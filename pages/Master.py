
import streamlit as st
import pandas as pd

def master_page():
    st.title("📦 Master List")
    password = st.text_input("Enter Admin Password", type="password")
    if password != "Nemo_63":
        st.warning("Unauthorized access")
        return

    try:
        df = pd.read_csv("Overall Master.csv")
        status_df = pd.read_csv("Status.csv")
        df = df.merge(status_df[["Item Code", "Status"]], on="Item Code", how="left")
        df["Status"] = df["Status"].fillna("Active")
        df["Mapping Status"] = df.apply(lambda x: "Mapped" if pd.notnull(x["Medicines Name"]) else "Unmapped", axis=1)

        search = st.text_input("Search Medicine")
        if search:
            df = df[df["Medicines Name"].str.contains(search, case=False, na=False)]

        edited = st.data_editor(df[["Item Code", "Medicines Name", "Unit", "Status", "Mapping Status"]], num_rows="dynamic")
        if st.button("Save Changes"):
            edited.to_csv("Overall Master.csv", index=False)
            st.success("Master updated")
    except Exception as e:
        st.error(f"Error: {e}")
