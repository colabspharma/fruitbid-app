import streamlit as st
import sqlite3
from components.sidebar import render_sidebar

DB_PATH = "fruitbid.db"

# ==========================
# ⚙️ Page setup
# ==========================
st.set_page_config(page_title="🏪 Marketplace", page_icon="🏪", layout="wide")

# ==========================
# 🔒 Login Guard (temporarily disabled for development)
# ==========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
    st.session_state.phone = "9999999999"
    st.session_state.user_name = "Developer"

# ==========================
# 🧭 Sidebar
# ==========================
selected_page = render_sidebar()

# ==========================
# 🌟 Page Content
# ==========================
st.title("🏪 Fruit Marketplace")
st.write(f"Welcome, **{st.session_state.user_name} ({st.session_state.phone})** 👋")
st.markdown("---")

# ==========================
# 🧺 Load Lots from Database
# ==========================
def fetch_lots():
    """Retrieve all available lots from DB."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT fruit_name, quantity, base_price, date_added FROM lots ORDER BY id DESC")
        return c.fetchall()

lots = fetch_lots()

# ==========================
# 📦 Display Lots
# ==========================
if lots:
    st.subheader("📦 Available Fruit Lots")

    for idx, (fruit, quantity, base_price, date_added) in enumerate(lots, start=1):
        with st.container():
            st.markdown(f"### 🍎 {fruit}")
            st.write(f"📦 Quantity: **{quantity}**")
            st.write(f"💰 Base Price: **₹{base_price}/kg**")
            st.caption(f"🕒 Added on {date_added}")
            st.button(f"Place Bid on {fruit}", key=f"bid_{idx}")
            st.markdown("---")
else:
    st.info("No fruit lots available yet. Please add some from the ⚙️ Admin Add Lot page.")

st.caption("💡 All lots shown here are pulled live from your `fruitbid.db` file.")
