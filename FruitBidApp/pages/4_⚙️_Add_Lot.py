import streamlit as st
import sqlite3
from datetime import datetime
from components.sidebar import render_sidebar

DB_PATH = "fruitbid.db"

# ==========================
# ⚙️ Page setup
# ==========================
st.set_page_config(page_title="⚙️ Add Lot (Admin)", page_icon="⚙️", layout="wide")

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
# 🗃️ Database Helpers
# ==========================
def init_db():
    """Ensure the lots table exists."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS lots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fruit_name TEXT,
                quantity TEXT,
                base_price REAL,
                date_added TEXT
            )
        """)
        conn.commit()

def add_lot(fruit_name, quantity, base_price):
    """Insert a new fruit lot into the database."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            INSERT INTO lots (fruit_name, quantity, base_price, date_added)
            VALUES (?, ?, ?, ?)
        """, (fruit_name, quantity, base_price, datetime.now().strftime("%Y-%m-%d %H:%M")))
        conn.commit()

# Initialize DB
init_db()

# ==========================
# 🌟 Page Content
# ==========================
st.title("⚙️ Admin — Add a New Fruit Lot")
st.write("Add fresh lots for bidding. (Admin use only)")
st.markdown("---")

# 🧺 Lot Entry Form
fruit_name = st.text_input("🍎 Fruit Name")
quantity = st.text_input("📦 Quantity (e.g. 10 kg, 1 crate)")
base_price = st.number_input("💰 Base Price (₹ per kg)", min_value=1.0, step=0.5)

# 🧾 Submit Button
if st.button("✅ Add Lot"):
    if fruit_name.strip() and quantity.strip():
        add_lot(fruit_name.strip(), quantity.strip(), base_price)
        st.success(f"✅ New lot added: **{fruit_name} ({quantity})** at ₹{base_price}/kg")
        st.balloons()  # 🎈 Nice visual feedback
        st.rerun()  # 🔁 Refresh the page to show the new entry
    else:
        st.warning("⚠️ Please fill in all required fields before adding the lot.")

# ==========================
# 📦 Current Lots Display
# ==========================
st.markdown("---")
st.subheader("📦 Current Active Lots")

with sqlite3.connect(DB_PATH) as conn:
    c = conn.cursor()
    c.execute("SELECT fruit_name, quantity, base_price, date_added FROM lots ORDER BY id DESC")
    rows = c.fetchall()

if rows:
    st.dataframe(
        [{"Fruit": r[0], "Quantity": r[1], "Base Price": f"₹{r[2]}", "Added": r[3]} for r in rows],
        use_container_width=True
    )
else:
    st.info("No lots added yet. Use the form above to create one.")

st.markdown("---")
st.caption("🧑‍🌾 Lots are stored in the local database (`fruitbid.db`). Bidding pages read from this table.")
