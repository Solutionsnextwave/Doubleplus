import streamlit as st

def login():
    st.markdown("<h2 style='color:#0071BC;'>🔐 Login to Double Plus</h2>", unsafe_allow_html=True)
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login", key="login_btn"):
        st.success("🎉 Logged in successfully! (UI Only)")