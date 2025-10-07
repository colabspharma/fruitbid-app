# =====================================================
# 🍎 app_web.py — Main FruitBid App Entry Point
# =====================================================

import os
import sqlite3
from datetime import datetime
import streamlit as st

# =====================================================
# 🍃 Sky Blue Theme with Animated Falling Leaves
# =====================================================
st.markdown("""
<style>
/* 🌤️ Background */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(180deg, #a7e9ff 0%, #d9f7ff 100%) !important;
    background-attachment: fixed !important;
    overflow: hidden;
}

/* 🌿 Leaf animation */
@keyframes fall {
    0% { transform: translateY(-10%) rotate(0deg); opacity: 1; }
    100% { transform: translateY(110vh) rotate(360deg); opacity: 0.7; }
}

.leaf {
    position: fixed;
    top: -10%;
    font-size: 1.8rem;
    animation: fall linear infinite;
    opacity: 0.9;
}

/* Random motion across screen */
.leaf:nth-child(1) { left: 5%; animation-duration: 7s; animation-delay: 0s; }
.leaf:nth-child(2) { left: 20%; animation-duration: 9s; animation-delay: 2s; }
.leaf:nth-child(3) { left: 35%; animation-duration: 8s; animation-delay: 1s; }
.leaf:nth-child(4) { left: 50%; animation-duration: 10s; animation-delay: 3s; }
.leaf:nth-child(5) { left: 65%; animation-duration: 11s; animation-delay: 0s; }
.leaf:nth-child(6) { left: 80%; animation-duration: 9s; animation-delay: 4s; }
.leaf:nth-child(7) { left: 95%; animation-duration: 8s; animation-delay: 1s; }

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.9);
    border-right: 2px solid #b2dfdb;
    backdrop-filter: blur(6px);
}

/* Hide Streamlit footer */
footer {visibility: hidden;}
</style>

<!-- 🍃 Animated leaves -->
<div class="leaf">🍃</div>
<div class="leaf">🍂</div>
<div class="leaf">🍃</div>
<div class="leaf">🍂</div>
<div class="leaf">🍃</div>
<div class="leaf">🍂</div>
<div class="leaf">🍃</div>
""", unsafe_allow_html=True)
st.markdown("""
<h1 style='text-align:center; color:#004d40; font-weight:800;
    text-shadow: 2px 2px 10px #a7ffeb;'>
<span style='color:#d50000;'>🍎</span> FruitBid — Fresh Produce, Fast Deals
</h1>
""", unsafe_allow_html=True)

# =====================================================
# 🎨 UI Components — Buttons, Cards, Inputs
# =====================================================
st.markdown("""
<style>

/* 🌱 Buttons */
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

/* 🍏 Input fields */
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

/* 🧺 Expanders */
.streamlit-expanderHeader {
    font-weight: 700;
    color: #004d40;
    background-color: rgba(224, 242, 241, 0.6);
    border-radius: 10px;
}

/* 🍇 Cards or containers */
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

/* ✨ Misc tweaks */
h2, h3 {
    color: #00695c !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

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

def reset_database():
    """Force delete any old or corrupted DB file."""
    db_path = "fruitbid.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        st.warning("🧹 Old database deleted. Fresh one will be created.")

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

def reset_database():
    """Force delete any old or corrupted DB file."""
    db_path = "fruitbid.db"
    if os.path.exists(db_path):
        os.remove(db_path)
        st.warning("🧹 Old database deleted. Fresh one will be created.")



def initialize_items():
    """Initialize fruit lots with safety check."""
    conn = sqlite3.connect("fruitbid.db")
    cursor = conn.cursor()

    # Drop and recreate table if schema mismatch or corruption occurs
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                quantity TEXT,
                base_price REAL,
                date_added TEXT
            )
        """)
        conn.commit()

        # Test select
        cursor.execute("SELECT COUNT(*) FROM lots")
        count = cursor.fetchone()[0]

    except sqlite3.OperationalError as e:
        st.warning(f"⚠️ Database issue detected: {e}. Recreating 'lots' table...")
        cursor.execute("DROP TABLE IF EXISTS lots")
        cursor.execute("""
            CREATE TABLE lots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT,
                quantity TEXT,
                base_price REAL,
                date_added TEXT
            )
        """)
        conn.commit()
        count = 0

    if count == 0:
        st.info("🌱 Seeding sample fruit lots...")
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
    # 🧹 Start fresh and initialize data
    reset_database()
    init_db()
    initialize_items()


    st.title("🍎 FruitBid — Fresh Produce, Fast Deals")


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

# =====================================================
# 🍎 Footer (subtle watermark)
# =====================================================
st.markdown("""
<hr style='margin-top:2rem; opacity:0.2;'>
<p style='text-align:center; color:#00695c; font-size:0.9rem;'>
Built with ❤️ using Streamlit — <b>FruitBid App</b>
</p>
""", unsafe_allow_html=True)
