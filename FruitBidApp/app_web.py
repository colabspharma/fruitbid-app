# =====================================================
# 🍎 app_web.py — Main FruitBid App Entry Point
# =====================================================

import streamlit as st
import sqlite3
from datetime import datetime

# =====================================================
# ✅ PAGE CONFIG (safe — only when running main app)
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
        # Avoid crash if already called in another page
        pass


# =====================================================
# 📂 IMPORTS
# =====================================================
try:
    from components.sidebar import render_sidebar
except ModuleNotFoundError:
    st.warning("⚠️ Sidebar missing — using fallback menu.")
    def render_sidebar():
        with st.sidebar:
            return st.radio(
                "Navigate:",
                ["🏠 Home", "🏪 Marketplace", "💼 My Bids", "⚙️ Add Lot (Admin)"]
            )


# =====================================================
# 📦 DATABASE SETUP
# =====================================================
def init_db():
    conn = sqlite3.connect("fruitbid.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            verified INTEGER DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            quantity TEXT,
            base_price REAL,
            date_added TEXT
        )
    """)

    cursor.execute("""
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


# =====================================================
# 🍎 INITIAL SAMPLE DATA (seed for demo)
# =====================================================
def initialize_items():
    conn = sqlite3.connect("fruitbid.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM lots")
    if cursor.fetchone()[0] == 0:
        sample_lots = [
            ("Apples", "100 kg", 120.0, datetime.now().strftime("%Y-%m-%d")),
            ("Bananas", "200 kg", 60.0, datetime.now().strftime("%Y-%m-%d")),
            ("Mangoes", "150 kg", 180.0, datetime.now().strftime("%Y-%m-%d")),
            ("Oranges", "180 kg", 90.0, datetime.now().strftime("%Y-%m-%d")),
        ]
        cursor.executemany(
            "INSERT INTO lots (item_name, quantity, base_price, date_added) VALUES (?, ?, ?, ?)",
            sample_lots
        )
        conn.commit()

    conn.close()


# =====================================================
# 🧩 DATABASE HELPERS
# =====================================================
def execute_query(query, params=()):
    conn = sqlite3.connect("fruitbid.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()


def fetch_all(query, params=()):
    conn = sqlite3.connect("fruitbid.db")
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results


# =====================================================
# 🌐 MAIN APP FUNCTION
# =====================================================
def main():
    init_db()
    initialize_items()

    st.title("🍉 FruitBid — Local Farmer Marketplace")

    selected_page = render_sidebar()

    # --------------------------
    # 🏠 HOME PAGE
    # --------------------------
    if selected_page == "🏠 Home":
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

    # --------------------------
    # 🏪 MARKETPLACE PAGE
    # --------------------------
    elif selected_page == "🏪 Marketplace":
        st.subheader("🏪 Marketplace — Active Lots")

        lots = fetch_all(
            "SELECT id, item_name, quantity, base_price, date_added FROM lots ORDER BY id DESC"
        )

        if not lots:
            st.warning("No lots available yet.")
        else:
            for lot_id, item_name, quantity, base_price, date_added in lots:
                with st.expander(f"{item_name} ({quantity}) — Base ₹{base_price}"):
                    st.write(f"📅 Added: {date_added}")

                    bid_amount = st.number_input(
                        f"Enter your bid for {item_name} (₹)",
                        min_value=float(base_price),
                        key=f"bid_{lot_id}"
                    )

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
                        """
                        SELECT user_name, bid_amount, timestamp
                        FROM bids WHERE lot_id = ?
                        ORDER BY bid_amount DESC LIMIT 3
                        """,
                        (lot_id,)
                    )
                    if top_bids:
                        st.write("📊 Top Bids:")
                        for user, amount, ts in top_bids:
                            st.write(f"• {user} — ₹{amount} ({ts})")

    # --------------------------
    # 💼 MY BIDS PAGE
    # --------------------------
    elif selected_page == "💼 My Bids":
        st.subheader("💼 My Bids")

        user_name = st.session_state.get("user_name")
        if not user_name:
            st.warning("Please enter your name on the Home page first.")
        else:
            my_bids = fetch_all(
                """
                SELECT lots.item_name, bids.bid_amount, bids.timestamp
                FROM bids
                JOIN lots ON bids.lot_id = lots.id
                WHERE bids.user_name = ?
                ORDER BY bids.timestamp DESC
                """,
                (user_name,)
            )

            if not my_bids:
                st.info("No bids placed yet.")
            else:
                for item, amount, ts in my_bids:
                    st.write(f"🍇 {item} — ₹{amount} at {ts}")

    # --------------------------
    # ⚙️ ADMIN PAGE
    # --------------------------
    elif selected_page == "⚙️ Add Lot (Admin)":
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
# 🚀 RUN THE APP
# =====================================================
if __name__ == "__main__":
    main()
