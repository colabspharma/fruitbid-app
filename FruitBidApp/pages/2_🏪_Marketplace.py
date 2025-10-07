# =====================================================
# 🏪 FruitBid Marketplace Page
# =====================================================

import streamlit as st
import sqlite3

# =====================================================
# ⚙️ Session State Initialization
# =====================================================
if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest"
if "phone" not in st.session_state:
    st.session_state.phone = "N/A"
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# =====================================================
# 📂 Imports & Setup
# =====================================================
try:
    from components.sidebar import render_sidebar
except ModuleNotFoundError:
    st.warning("⚠️ Sidebar component missing. Ensure `components/sidebar.py` exists.")
    
    def render_sidebar():
        """Fallback sidebar if component not found."""
        st.sidebar.title("Navigation")
        st.sidebar.write("🏠 Home")
        return None

DB_PATH = "fruitbid.db"

# =====================================================
# 🖥️ UI — Marketplace Page
# =====================================================
st.title("🏪 Fruit Marketplace")

# Sidebar render
render_sidebar()

# Welcome section
st.write(f"Welcome, **{st.session_state.user_name} ({st.session_state.phone})** 👋")

# Placeholder for future marketplace content
st.info("Browse available fruit lots below. Coming soon 🍌🍎🍇")


# =====================================================
# ⚙️ Session State Initialization
# =====================================================
if "user_name" not in st.session_state:
    st.session_state.user_name = "Guest"
if "phone" not in st.session_state:
    st.session_state.phone = "N/A"
if "is_logged_in" not in st.session_state:
    st.session_state.is_logged_in = False

# =====================================================
# 🔒 Developer Login (temporary bypass)
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
    st.session_state.user_name = "Developer"
    st.session_state.phone = "9999999999"


# =====================================================
# 🧭 Sidebar
# =====================================================
selected_page = render_sidebar("marketplace")



# =====================================================
# 🌟 Page Header
# =====================================================
st.title("🏪 Fruit Marketplace")
st.write(f"Welcome, **{st.session_state.user_name} ({st.session_state.phone})** 👋")
st.markdown("---")


# =====================================================
# 🧺 Fetch Lots from Database
# =====================================================
def fetch_lots():
    """Retrieve all available fruit lots from the database."""
    try:
        with sqlite3.connect(DB_PATH) as conn:
            c = conn.cursor()
            c.execute("""
                SELECT item_name, quantity, base_price, date_added 
                FROM lots ORDER BY id DESC
            """)
            return c.fetchall()
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []


lots = fetch_lots()


# =====================================================
# 📦 Display Available Lots
# =====================================================
if lots:
    st.subheader("📦 Available Fruit Lots")

    for idx, (fruit, quantity, base_price, date_added) in enumerate(lots, start=1):
        with st.container():
            st.markdown(f"### 🍎 {fruit}")
            st.write(f"📦 **Quantity:** {quantity}")
            st.write(f"💰 **Base Price:** ₹{base_price}/kg")
            st.caption(f"🕒 Added on {date_added}")

            # Placeholder for bidding action
            st.button(f"💰 Place Bid on {fruit}", key=f"bid_{idx}")
            st.markdown("---")

else:
    st.info("No fruit lots available yet. Please add some from the ⚙️ Admin Add Lot page.")


# =====================================================
# 🧾 Footer Note
# =====================================================
st.caption("💡 All lots shown here are fetched live from `fruitbid.db`.")
