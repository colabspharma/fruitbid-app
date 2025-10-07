# =====================================================
# ⚙️ Admin — Add Fruit Lots | FruitBid App
# =====================================================

import streamlit as st
import sqlite3
from datetime import datetime
from components.sidebar import render_sidebar

DB_PATH = "fruitbid.db"


# =====================================================
# ⚙️ PAGE SETUP
# =====================================================

# Developer session (temporary bypass)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
    st.session_state.user_name = "Developer"
    st.session_state.phone = "9999999999"


# =====================================================
# 🧭 SIDEBAR
# =====================================================
render_sidebar()


# =====================================================
# 🗃️ DATABASE HELPERS
# =====================================================
def init_db():
    """Create the lots table if it doesn’t exist."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS lots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity TEXT NOT NULL,
                base_price REAL NOT NULL,
                date_added TEXT
            )
        """)
        conn.commit()


def add_lot(item_name: str, quantity: str, base_price: float):
    """Insert a new fruit lot into the database."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO lots (item_name, quantity, base_price, date_added)
            VALUES (?, ?, ?, ?)
        """, (item_name, quantity, base_price, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()


def fetch_lots():
    """Retrieve all lots from the database."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("SELECT item_name, quantity, base_price, date_added FROM lots ORDER BY id DESC")
        return c.fetchall()


# Initialize database
init_db()


# =====================================================
# 🌟 PAGE CONTENT
# =====================================================
st.title("⚙️ Admin — Add a New Fruit Lot")
st.write("Add fresh fruit lots for bidding. (Admin use only)")
st.markdown("---")


# =====================================================
# 🧺 ADD LOT FORM
# =====================================================
with st.form("add_lot_form", clear_on_submit=True):
    item_name = st.text_input("🍎 Fruit Name", placeholder="e.g. Mango (Alphonso)")
    quantity = st.text_input("📦 Quantity", placeholder="e.g. 10 kg, 1 crate")
    base_price = st.number_input("💰 Base Price (₹ per kg)", min_value=1.0, step=0.5)

    submitted = st.form_submit_button("✅ Add Lot")

    if submitted:
        if item_name.strip() and quantity.strip():
            add_lot(item_name.strip(), quantity.strip(), base_price)
            st.success(f"✅ New lot added: **{item_name} ({quantity})** at ₹{base_price}/kg")
            st.balloons()
            st.rerun()
        else:
            st.warning("⚠️ Please fill in all required fields before adding the lot.")


# =====================================================
# 📦 CURRENT LOTS
# =====================================================
st.markdown("---")
st.subheader("📦 Current Active Lots")

rows = fetch_lots()

if rows:
    st.dataframe(
        [
            {"Fruit": r[0], "Quantity": r[1], "Base Price": f"₹{r[2]}/kg", "Added": r[3]}
            for r in rows
        ],
        use_container_width=True,
    )
else:
    st.info("No lots added yet. Use the form above to create one.")

st.markdown("---")
st.caption("🧑‍🌾 All lots are stored in `fruitbid.db`. Marketplace and My Bids pages read from this table.")
