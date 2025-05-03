
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Double Plus | Replenishment", layout="wide")
st.markdown("<style>div.stButton > button {background-color:#0071BC; color:white;}</style>", unsafe_allow_html=True)
st.image("Double Plus Logo.png", width=180)
st.title("🏪 Welcome to Double Plus Replenishment System")

st.markdown("#### 📌 This system helps calculate **Replenishment** and **Procurement** based on 6-month sales data and daily stock inputs.")
st.markdown("""---
### 📘 Min/Max Logic
- **Min Stock** = Average Weekly Sale x 2 weeks
- **Max Stock** = Average Weekly Sale x 4 weeks
- **Replenishment** = Issued when store stock ≤ Min
- Loose stock is converted to **strips** for tablets and capsules.
""")
st.success("Use the left sidebar to navigate to Admin, Master, or Report section.")
    