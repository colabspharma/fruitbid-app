# app_web.py
import streamlit as st
import sqlite3
from datetime import datetime

# --------------------------
# DATABASE SETUP
# --------------------------
def init_db():
    conn = sqlite3.connect("fruitbid.db")
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
    conn.close()

# --------------------------
# HELPER FUNCTIONS
# --------------------------
def add_user(name, phone):
    conn = sqlite3.connect("fruitbid.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()

def get_lots():
    conn = sqlite3.connect("fruitbid.db")
    c = conn.cursor()
    c.execute("SELECT * FROM lots")
    lots = c.fetchall()
    conn.close()
    return lots

def add_lot(fruit_name, quantity, base_price):
    conn = sqlite3.connect("fruitbid.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO lots (fruit_name, quantity, base_price, date_added) VALUES (?, ?, ?, ?)",
        (fruit_name, quantity, base_price, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()
    conn.close()

def place_bid(user_name, lot_id, bid_amount):
    conn = sqlite3.connect("fruitbid.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO bids (user_name, lot_id, bid_amount, timestamp) VALUES (?, ?, ?, ?)",
        (user_name, lot_id, bid_amount, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    )
    conn.commit()
    conn.close()

def get_bids_for_lot(lot_id):
    conn = sqlite3.connect("fruitbid.db")
    c = conn.cursor()
    c.execute("SELECT user_name, bid_amount, timestamp FROM bids WHERE lot_id = ? ORDER BY bid_amount DESC", (lot_id,))
    bids = c.fetchall()
    conn.close()
    return bids

# --------------------------
# MAIN APP
# --------------------------
def main():
    st.set_page_config(page_title="🍉 FruitBid", layout="wide")
    st.title("🍉 FruitBid — Local Farmer Marketplace")

    init_db()

    # Sidebar navigation
    menu = ["Home", "Marketplace", "My Bids", "Add Lot (Admin)"]
    choice = st.sidebar.selectbox("Navigate", menu)

    # --------------------------
    # HOME PAGE (TEMPORARY LOGIN SKIPPED)
    # --------------------------
    if choice == "Home":
        st.subheader("👋 Welcome to FruitBid")
        st.info("OTP login is disabled temporarily for testing.")
        name = st.text_input("Your Name")
        phone = st.text_input("Phone Number (for records only)", max_chars=10)
        if st.button("Enter Marketplace"):
            if name.strip() == "":
                st.warning("Please enter your name.")
            else:
                st.session_state["user_name"] = name
                st.session_state["phone"] = phone
                st.success(f"Welcome, {name}! Use the sidebar to browse the Marketplace.")
    
    # --------------------------
    # MARKETPLACE PAGE
    # --------------------------
    elif choice == "Marketplace":
        st.subheader("🏪 Marketplace — Active Lots")

        lots = get_lots()
        if not lots:
            st.warning("No lots available yet.")
        else:
            for lot in lots:
                lot_id, fruit_name, quantity, base_price, date_added = lot
                with st.expander(f"{fruit_name} ({quantity}) — Base ₹{base_price}"):
                    st.write(f"📅 Added: {date_added}")
                    st.write("💬 Place your bid below:")
                    bid_amount = st.number_input("Enter your bid (₹)", min_value=base_price, key=f"bid_{lot_id}")
                    if st.button(f"Submit Bid for Lot {lot_id}"):
                        user_name = st.session_state.get("user_name", "Guest")
                        place_bid(user_name, lot_id, bid_amount)
                        st.success(f"✅ Bid placed successfully for ₹{bid_amount} on {fruit_name}!")
                    bids = get_bids_for_lot(lot_id)
                    if bids:
                        st.write("📊 Current Top Bids:")
                        for b in bids[:3]:
                            st.write(f"• {b[0]} — ₹{b[1]} ({b[2]})")
    
    # --------------------------
    # MY BIDS PAGE
    # --------------------------
    elif choice == "My Bids":
        st.subheader("💼 My Bids")
        user_name = st.session_state.get("user_name", None)
        if not user_name:
            st.warning("Please enter your name on the Home page first.")
        else:
            conn = sqlite3.connect("fruitbid.db")
            c = conn.cursor()
            c.execute("SELECT lot_id, bid_amount, timestamp FROM bids WHERE user_name = ?", (user_name,))
            rows = c.fetchall()
            conn.close()
            if not rows:
                st.info("No bids placed yet.")
            else:
                for row in rows:
                    lot_id, bid_amount, timestamp = row
                    st.write(f"Lot #{lot_id} — ₹{bid_amount} at {timestamp}")

    # --------------------------
    # ADMIN PAGE
    # --------------------------
    elif choice == "Add Lot (Admin)":
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

# --------------------------
if __name__ == "__main__":
    main()
