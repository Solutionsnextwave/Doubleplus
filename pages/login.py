import streamlit as st

def login_page():
    st.markdown("<h2 style='color:#0071BC;'>Login</h2>", unsafe_allow_html=True)
    st.text_input("Username")
    st.text_input("Password", type="password")
    st.button("Login")