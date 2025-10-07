# app_web.py
import streamlit as st
import sqlite3
from datetime import datetime
from components.sidebar import render_sidebar  # ✅ sidebar integration

DB_PATH = "fruitbid.db"

# ==========================
# 🗃️ DATABASE SETUP
# ==========================
def init_db():
    """Initialize SQLite tables if not already created."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS lots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fruit_name TEXT,
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


# ==========================
# ⚙️ HELPER FUNCTIONS
# ==========================
def execute_query(query, params=(), fetch=False):
    """Reusable DB helper for SELECT / INSERT / UPDATE."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute(query, params)
        data = c.fetchall() if fetch else None
        conn.commit()
    return data


def add_user(name, phone):
    execute_query(
        "INSERT INTO users (name, phone) VALUES (?, ?)",
        (name, phone)
    )


def get_lots():
    return execute_query("SELECT * FROM lots", fetch=True)


def add_lot(fruit_name, quantity, base_price):
    execute_query(
        "INSERT INTO lots (fruit_name, quantity, base_price, date_added) VALUES (?, ?, ?, ?)",
        (fruit_name, quantity, base_price, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )


def place_bid(user_name, lot_id, bid_amount):
    execute_query(
        "INSERT INTO bids (user_name, lot_id, bid_amount, timestamp) VALUES (?, ?, ?, ?)",
        (user_name, lot_id, bid_amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )


def get_bids_for_lot(lot_id):
    return execute_query(
        "SELECT user_name, bid_amount, timestamp FROM bids WHERE lot_id = ? ORDER BY bid_amount DESC",
        (lot_id,),
        fetch=True
    )


# ==========================
# 🌐 MAIN APP
# ==========================
def main():
    st.set_page_config(page_title="🍉 FruitBid", layout="wide")
    st.title("🍉 FruitBid — Local Farmer Marketplace")

    init_db()

    # Sidebar navigation (imported from components)
    selected_page = render_sidebar()

    # --------------------------
    # 🏠 HOME PAGE
    # --------------------------
    if selected_page == "🏠 Home":
        st.subheader("👋 Welcome to FruitBid")
        st.info("OTP login is temporarily disabled for testing.")

        name = st.text_input("Your Name")
        phone = st.text_input("Phone Number (for records only)", max_chars=10)

        if st.button("Enter Marketplace"):
            if not name.strip():
                st.warning("Please enter your name.")
            else:
                st.session_state["user_name"] = name.strip()
                st.session_state["phone"] = phone.strip()
                st.success(f"Welcome, {name}! Use the sidebar to explore the Marketplace.")

    # --------------------------
    # 🏪 MARKETPLACE PAGE
    # --------------------------
    elif selected_page == "🏪 Marketplace":
        st.subheader("🏪 Marketplace — Active Lots")

        lots = get_lots()
        if not lots:
            st.warning("No lots available yet.")
        else:
            for lot in lots:
                lot_id, fruit_name, quantity, base_price, date_added = lot
                with st.expander(f"{fruit_name} ({quantity}) — Base ₹{base_price}"):
                    st.write(f"📅 Added: {date_added}")

                    bid_amount = st.number_input(
                        f"Enter your bid for {fruit_name} (₹)",
                        min_value=base_price,
                        key=f"bid_{lot_id}"
                    )

                    if st.button(f"💰 Submit Bid for {fruit_name}", key=f"submit_{lot_id}"):
                        user_name = st.session_state.get("user_name", "Guest")
                        place_bid(user_name, lot_id, bid_amount)
                        st.success(f"✅ ₹{bid_amount} bid placed on {fruit_name}!")

                    bids = get_bids_for_lot(lot_id)
                    if bids:
                        st.write("📊 Top Bids:")
                        for b in bids[:3]:
                            st.write(f"• {b[0]} — ₹{b[1]} ({b[2]})")

    # --------------------------
    # 💼 MY BIDS PAGE
    # --------------------------
    elif selected_page == "💼 My Bids":
        st.subheader("💼 My Bids")

        user_name = st.session_state.get("user_name")
        if not user_name:
            st.warning("Please enter your name on the Home page first.")
        else:
            rows = execute_query(
                "SELECT lot_id, bid_amount, timestamp FROM bids WHERE user_name = ?",
                (user_name,),
                fetch=True
            )
            if not rows:
                st.info("No bids placed yet.")
            else:
                for lot_id, bid_amount, timestamp in rows:
                    st.write(f"Lot #{lot_id} — ₹{bid_amount} at {timestamp}")

    # --------------------------
    # ⚙️ ADMIN PAGE
    # --------------------------
    elif selected_page == "⚙️ Add Lot (Admin)":
        st.subheader("⚙️ Admin: Add a New Lot")

        fruit_name = st.text_input("Fruit Name")
        quantity = st.text_input("Quantity (e.g. 10 kg, 1 box)")
        base_price = st.number_input("Base Price (₹)", min_value=1.0, step=0.5)

        if st.button("Add Lot"):
            if fruit_name and quantity:
                add_lot(fruit_name, quantity, base_price)
                st.success(f"✅ Added new lot: {fruit_name} ({quantity}) at ₹{base_price}")
            else:
                st.warning("Please fill in all fields.")


# ==========================
# 🚀 RUN
# ==========================
if __name__ == "__main__":
    main()
