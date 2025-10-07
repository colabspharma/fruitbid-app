# =====================================================
# 🍇 FruitBid Dashboard
# =====================================================

import streamlit as st

# ⚙️ PAGE CONFIG — must be FIRST Streamlit command

# Try importing sidebar safely
try:
    from components.sidebar import render_sidebar
except ModuleNotFoundError:
    st.warning("⚠️ Sidebar component not found. Make sure `components/sidebar.py` exists.")
    def render_sidebar():
        return "🏠 Home"

# =====================================================
# 🔒 Developer Login (TEMPORARILY DISABLED)
# =====================================================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = True
    st.session_state.user_name = "Developer"
    st.session_state.phone = "9999999999"

# =====================================================
# 🧭 Sidebar Navigation
# =====================================================
selected_page = render_sidebar()

# =====================================================
# 🌟 Page Header
# =====================================================
st.title("🍇 FruitBid Dashboard")
st.write(f"Welcome back, **{st.session_state.user_name} ({st.session_state.phone})** 👋")
st.markdown("---")

# =====================================================
# 📊 Dashboard Metrics
# =====================================================
col1, col2, col3 = st.columns(3)
col1.metric("Active Bids", "3", "↑ 1")
col2.metric("Fruits Won", "12 kg", "🍎 +2")
col3.metric("Wallet Balance", "₹ 2,450", "💰")

st.markdown("---")

# =====================================================
# 🛍️ Current Fruit Lots
# =====================================================
st.subheader("🛍️ Current Fruit Lots")

lots = [
    {"Fruit": "Mango (Alphonso)", "Current Bid": "₹ 120/kg", "Time Left": "10 min"},
    {"Fruit": "Banana (Robusta)", "Current Bid": "₹ 45/kg", "Time Left": "30 min"},
    {"Fruit": "Apple (Shimla)", "Current Bid": "₹ 150/kg", "Time Left": "5 min"},
]

st.dataframe(lots, use_container_width=True)

st.markdown("---")
st.caption("📈 More analytics, charts, and price insights coming soon!")
