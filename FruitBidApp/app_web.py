# =====================================================
# 🍎 app_web.py — Main FruitBid App Entry Point (Fixed)
# =====================================================

import os
import sqlite3
from datetime import datetime
import streamlit as st

# =====================================================
# ✅ PAGE CONFIG
# =====================================================
if "page_configured" not in st.session_state:
    try:
        st.set_page_config(
            page_title="🍎 FruitBid App",
            page_icon="🍇",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.session_state["page_configured"] = True
    except st.errors.StreamlitAPIException:
        pass


# =====================================================
# 🎨 THEME & STYLES
# =====================================================
st.markdown("""
<style>
div.stButton > button {
    background: linear-gradient(90deg, #26a69a, #80cbc4);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    transition: all 0.3s ease-in-out;
    box-shadow: 0px 3px 10px rgba(38, 166, 154, 0.4);
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #00796b, #4db6ac);
    transform: translateY(-2px);
    box-shadow: 0px 6px 12px rgba(0, 121, 107, 0.3);
}
input, textarea, select {
    border-radius: 8px !important;
    border: 1px solid #b2dfdb !important;
    background-color: #ffffff !important;
    color: #004d40 !important;
}
input:focus, textarea:focus, select:focus {
    border: 1px solid #26a69a !important;
    box-shadow: 0 0 0 3px rgba(38, 166, 154, 0.2) !important;
    outline: none !important;
}
.streamlit-expanderHeader {
    font-weight: 700;
    color: #004d40;
    background-color: rgba(224, 242, 241, 0.6);
    border-radius: 10px;
}
.block-container {
    padding: 2rem 3rem;
}
[data-testid="stVerticalBlock"] > div {
    background-color: rgba(255,255,255,0.7);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 3px 6px rgba(0,0,0,0.05);
}
h2, h3 {
    color: #00695c !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# 📦 DATABASE UTILITIES
# =====================================================

DB_PATH = "fruitbid.db"

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            verified INTEGER DEFAULT 0
        )
    """)
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
            user_name TEXT,
            lot_id INTEGER,
            bid_amount REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()


def seed_data():
    """Insert demo fruit lots only if table is empty."""
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM lots")
    count = c.fetchone()[0]

    if count == 0:
        st.info("🌱 Seeding sample fruit lots...")
        lots = [
            ("Apples", "100 kg", 120.0, datetime.now().strftime("%Y-%m-%d")),
            ("Bananas", "200 kg", 60.0, datetime.now().strftime("%Y-%m-%d")),
            ("Mangoes", "150 kg", 180.0, datetime.now().strftime("%Y-%m-%d")),
            ("Oranges", "180 kg", 90.0, datetime.now().strftime("%Y-%m-%d")),
        ]
        c.executemany(
            "INSERT INTO lots (item_name, quantity, base_price, date_added) VALUES (?, ?, ?, ?)",
            lots
        )
        conn.commit()

    conn.close()


def execute_query(query, params=()):
    conn = get_conn()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def fetch_all(query, params=()):
    conn = get_conn()
    c = conn.cursor()
    c.execute(query, params)
    data = c.fetchall()
    conn.close()
    return data


# =====================================================
# 📂 SIDEBAR IMPORT OR FALLBACK
# =====================================================
try:
    from components.sidebar import render_sidebar
except ModuleNotFoundError:
    def render_sidebar():
        with st.sidebar:
            return st.radio(
                "Navigate:",
                ["🏠 Home", "🏪 Marketplace", "💼 My Bids", "⚙️ Add Lot (Admin)"]
            )


# =====================================================
# 🚀 MAIN
# =====================================================
def main():
    if "initialized" not in st.session_state:
        init_db()
        seed_data()
        st.session_state["initialized"] = True

    st.title("🍎 FruitBid — Fresh Produce, Fast Deals")
    page = render_sidebar()

    # HOME
    if page == "🏠 Home":
        st.subheader("👋 Welcome to FruitBid")
        st.info("OTP login temporarily disabled for testing.")
        name = st.text_input("Your Name")
        phone = st.text_input("Phone Number (for records only)", max_chars=10)
        if st.button("Enter Marketplace"):
            if not name.strip():
                st.warning("Please enter your name.")
            else:
                st.session_state["user_name"] = name.strip()
                st.session_state["phone"] = phone.strip()
                st.success(f"Welcome, {name}! Use the sidebar to explore the Marketplace.")

    # MARKETPLACE
    elif page == "🏪 Marketplace":
        st.subheader("🏪 Marketplace — Active Lots")
        lots = fetch_all("SELECT id, item_name, quantity, base_price, date_added FROM lots ORDER BY id DESC")
        if not lots:
            st.warning("No lots available yet.")
        else:
            for lot_id, item_name, quantity, base_price, date_added in lots:
                with st.expander(f"{item_name} ({quantity}) — Base ₹{base_price}"):
                    st.write(f"📅 Added: {date_added}")
                    bid_amount = st.number_input(f"Enter your bid for {item_name} (₹)", min_value=float(base_price), key=f"bid_{lot_id}")
                    if st.button(f"💰 Submit Bid for {item_name}", key=f"submit_{lot_id}"):
                        user_name = st.session_state.get("user_name", "Guest")
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        execute_query(
                            "INSERT INTO bids (user_name, lot_id, bid_amount, timestamp) VALUES (?, ?, ?, ?)",
                            (user_name, lot_id, bid_amount, timestamp)
                        )
                        st.success(f"✅ ₹{bid_amount} bid placed on {item_name}!")

                    # Show top 3 bids
                    top_bids = fetch_all(
                        "SELECT user_name, bid_amount, timestamp FROM bids WHERE lot_id=? ORDER BY bid_amount DESC LIMIT 3",
                        (lot_id,)
                    )
                    if top_bids:
                        st.write("📊 Top Bids:")
                        for user, amt, ts in top_bids:
                            st.write(f"• {user} — ₹{amt} ({ts})")

    # MY BIDS
    elif page == "💼 My Bids":
        st.subheader("💼 My Bids")
        user_name = st.session_state.get("user_name")
        if not user_name:
            st.warning("Please enter your name on the Home page first.")
        else:
            my_bids = fetch_all("""
                SELECT lots.item_name, bids.bid_amount, bids.timestamp
                FROM bids
                JOIN lots ON bids.lot_id = lots.id
                WHERE bids.user_name = ?
                ORDER BY bids.timestamp DESC
            """, (user_name,))
            if not my_bids:
                st.info("No bids placed yet.")
            else:
                for item, amt, ts in my_bids:
                    st.write(f"🍇 {item} — ₹{amt} at {ts}")

    # ADMIN
    elif page == "⚙️ Add Lot (Admin)":
        st.subheader("⚙️ Admin: Add a New Lot")
        item_name = st.text_input("Fruit Name")
        quantity = st.text_input("Quantity (e.g. 10 kg, 1 box)")
        base_price = st.number_input("Base Price (₹)", min_value=1.0, step=0.5)
        if st.button("Add Lot"):
            if item_name and quantity:
                execute_query(
                    "INSERT INTO lots (item_name, quantity, base_price, date_added) VALUES (?, ?, ?, ?)",
                    (item_name, quantity, base_price, datetime.now().strftime("%Y-%m-%d"))
                )
                st.success(f"✅ Added new lot: {item_name} ({quantity}) at ₹{base_price}")
            else:
                st.warning("Please fill in all fields.")


# =====================================================
# 🏁 RUN
# =====================================================
if __name__ == "__main__":
    main()

st.markdown("""
<hr style='margin-top:2rem; opacity:0.2;'>
<p style='text-align:center; color:#00695c; font-size:0.9rem;'>
Built with ❤️ using Streamlit — <b>FruitBid App</b>
</p>
""", unsafe_allow_html=True)
