# =====================================================
# 💼 My Bids — FruitBid App
# =====================================================

import streamlit as st
import sqlite3
from datetime import datetime

# =====================================================
# ✅ PAGE CONFIG (must be the first Streamlit command)
# =====================================================
st.set_page_config(page_title="💼 My Bids", page_icon="💼", layout="wide")

# =====================================================
# 📂 IMPORTS
# =====================================================
try:
    from components.sidebar import render_sidebar
    from app_web import init_db  # Database setup function
except ModuleNotFoundError:
    st.warning("⚠️ Missing imports — using fallback menu and DB init.")
    def render_sidebar():
        with st.sidebar:
            return st.radio("Navigate:", ["🏠 Home", "🏪 Marketplace", "💼 My Bids", "⚙️ Add Lot (Admin)"])
    def init_db(): pass

DB_PATH = "fruitbid.db"

# =====================================================
# ⚙️ INITIAL SETUP
# =====================================================
init_db()  # Ensure tables exist before proceeding


# =====================================================
# 🔒 TEMPORARY DEVELOPER LOGIN (for testing)
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

st.subheader("🧑‍💻 Developer Login (temporary)")

DEV_USERNAME = "admin"
DEV_PASSWORD = "fruitbid123"

if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == DEV_USERNAME and password == DEV_PASSWORD:
            st.session_state.logged_in = True
            st.session_state.user_name = "Developer"
            st.session_state.phone = "9999999999"
            st.success("✅ Developer logged in successfully!")
        else:
            st.error("❌ Invalid username or password")
    st.stop()  # Stop execution until logged in


# =====================================================
# 🧭 SIDEBAR
# =====================================================
render_sidebar()


# =====================================================
# 🌟 PAGE HEADER
# =====================================================
st.title("💼 My Bids")

user_name = st.session_state.get("user_name", "Guest")
user_phone = st.session_state.get("phone", "Unknown")

st.write(f"Welcome back, **{user_name} ({user_phone})** 👋")
st.markdown("---")


# =====================================================
# 🧺 DATABASE HELPERS
# =====================================================
def get_available_lots():
    """Fetch all fruit lots."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT item_name, base_price 
            FROM lots ORDER BY id DESC
        """)
        return c.fetchall()


def create_bids_table():
    """Ensure bids table exists."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS bids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_phone TEXT,
                item_name TEXT,
                bid_price REAL,
                bid_time TEXT
            )
        """)
        conn.commit()


def insert_bid(phone, item_name, bid_price):
    """Insert a new bid."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO bids (user_phone, item_name, bid_price, bid_time)
            VALUES (?, ?, ?, ?)
        """, (
            phone,
            item_name,
            bid_price,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()


def get_user_bids(phone):
    """Fetch all bids by a user."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT item_name, bid_price, bid_time
            FROM bids WHERE user_phone = ? ORDER BY id DESC
        """, (phone,))
        return c.fetchall()


# =====================================================
# 💰 PLACE A NEW BID
# =====================================================
create_bids_table()
lots = get_available_lots()

if lots:
    st.subheader("💰 Place a New Bid")

    item_options = [lot[0] for lot in lots]
    selected_item = st.selectbox("Select Fruit Lot", item_options)

    base_price = next(lot[1] for lot in lots if lot[0] == selected_item)
    bid_price = st.number_input(
        f"Enter your bid (₹/kg) — Base price ₹{base_price}",
        min_value=1.0,
        step=1.0,
    )

    if st.button("✅ Submit Bid"):
        insert_bid(user_phone, selected_item, bid_price)
        st.success(f"🎉 Bid of ₹{bid_price}/kg placed for **{selected_item}** successfully!")
else:
    st.info("No fruit lots available yet. Please add some from the ⚙️ Admin Add Lot page.")

st.markdown("---")


# =====================================================
# 📊 DISPLAY USER’S BIDS
# =====================================================
user_bids = get_user_bids(user_phone)

st.subheader("📋 Your Bids")

if user_bids:
    st.dataframe(
        [{"Fruit": f, "Bid (₹/kg)": b, "Time": t} for f, b, t in user_bids],
        use_container_width=True
    )
else:
    st.info("You haven’t placed any bids yet.")

st.caption("💡 All bids are stored in `fruitbid.db` for persistence across sessions.")
