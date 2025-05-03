import streamlit as st
from pages import login, dashboard, inventory, reports, users

# Placeholder for streamlit_app.py styled with Rhombus kit in future implementation
st.set_page_config(page_title="Double Plus Dashboard", layout="wide")
st.title("Double Plus | Dashboard")
st.sidebar.success("Use the menu to navigate.")