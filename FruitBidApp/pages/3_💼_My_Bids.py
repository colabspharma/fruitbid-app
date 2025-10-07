import streamlit as st
import sqlite3
from datetime import datetime
from components.sidebar import render_sidebar

DB_PATH = "fruitbid.db"

# ==========================
# ⚙️ Page setup
# ==========================
st.set_page_config(page_title="💼 My Bids", page_icon="💼", layout="wide")

# ==========================
# 🔒 Developer Login (temporary)
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
# 🧱 Database Setup
# ==========================
def init_db():
    """Ensure required tables exist with consistent column names."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS lots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                quantity TEXT,
                base_price REAL,
                date_added TEXT
            )
        """)
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

init_db()

# ==========================
# 🌟 Page Header
# ==========================
st.title("💼 My Bids")
st.write(f"Welcome back, **{st.session_state.user_name} ({st.session_state.phone})** 👋")
st.markdown("---")

# ==========================
# 📦 Fetch Available Lots
# ==========================
def get_available_lots():
    """Fetch all fruit lots from database."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT item_name, base_price FROM lots ORDER BY id DESC")
        return c.fetchall()

lots = get_available_lots()

# ==========================
# 💰 Place a New Bid
# ==========================
if lots:
    st.subheader("💰 Place a New Bid")

    item_options = [lot[0] for lot in lots]
    selected_item = st.selectbox("Select Fruit Lot", item_options)
    base_price = next(lot[1] for lot in lots if lot[0] == selected_item)

    bid_price = st.number_input(
        f"Enter your bid (₹/kg) — Base price ₹{base_price}", 
        min_value=1, 
        step=1
    )

    if st.button("✅ Submit Bid"):
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                INSERT INTO bids (user_phone, item_name, bid_price, bid_time)
                VALUES (?, ?, ?, ?)
            """, (
                st.session_state.phone,
                selected_item,
                bid_price,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))
            conn.commit()
        st.success(f"🎉 Bid of ₹{bid_price}/kg placed for **{selected_item}** successfully!")
else:
    st.info("No fruit lots available yet. Please add some from the ⚙️ Admin Add Lot page.")

st.markdown("---")

# ==========================
# 📊 Display User’s Bids
# ==========================
def get_user_bids(user_phone):
    """Retrieve all bids placed by this user."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            SELECT item_name, bid_price, bid_time
            FROM bids WHERE user_phone = ? ORDER BY id DESC
        """, (user_phone,))
        return c.fetchall()

user_bids = get_user_bids(st.session_state.phone)

st.subheader("📋 Your Bids")

if user_bids:
    st.dataframe(
        [{"Fruit": f, "Bid (₹/kg)": b, "Time": t} for f, b, t in user_bids],
        use_container_width=True
    )
else:
    st.info("You haven’t placed any bids yet.")

st.caption("💡 All bids are stored in `fruitbid.db` for persistence across sessions.")
