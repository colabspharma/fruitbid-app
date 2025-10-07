import streamlit as st
from FruitBidApp.pages.components.sidebar import render_sidebar

st.set_page_config(page_title="FruitBid Dashboard", page_icon="🍇", layout="wide")

# 🔒 Login Guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please log in first from the main page.")
    st.stop()

# 🧭 Sidebar
render_sidebar()

# 🌟 Page Content
st.title("🍇 FruitBid Dashboard")
st.write(f"Welcome back, **{st.session_state.phone}** 👋")
st.markdown("---")

col1, col2, col3 = st.columns(3)
col1.metric("Active Bids", "3", "↑ 1")
col2.metric("Fruits Won", "12 kg", "🍎 +2")
col3.metric("Wallet Balance", "₹2 450", "💰")

st.markdown("### 🛍️ Current Fruit Lots")
st.dataframe(
    [
        {"Fruit": "Mango (Alphonso)", "Current Bid": "₹120/kg", "Time Left": "10 min"},
        {"Fruit": "Banana (Robusta)", "Current Bid": "₹45/kg", "Time Left": "30 min"},
        {"Fruit": "Apple (Shimla)", "Current Bid": "₹150/kg", "Time Left": "5 min"},
    ],
    use_container_width=True,
)

st.markdown("---")
st.caption("📈 More analytics and charts coming soon!")

import streamlit as st

# 🧩 Page setup
st.set_page_config(page_title="FruitBid Dashboard", page_icon="🍇", layout="wide")

# 🔒 1️⃣ Login Guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please log in first from the main page.")
    st.stop()

# 🧭 2️⃣ Sidebar Section
st.sidebar.title("🍇 FruitBid")
st.sidebar.markdown(f"**👤 {st.session_state.phone}**")
st.sidebar.markdown("---")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.otp_sent = False
    st.session_state.phone = ""
    st.info("You’ve been logged out successfully.")
    st.switch_page("app_web.py")

# 🌟 3️⃣ Page Content
st.title("🍇 FruitBid Dashboard")
st.write(f"Welcome back, **{st.session_state.phone}** 👋")
st.markdown("---")

# 📊 Dashboard Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Active Bids", "3", "↑ 1")
col2.metric("Fruits Won", "12 kg", "🍎 +2")
col3.metric("Wallet Balance", "₹2 450", "💰")

# 🛍️ Current Fruit Lots
st.markdown("### 🛍️ Current Fruit Lots")
st.dataframe(
    [
        {"Fruit": "Mango (Alphonso)", "Current Bid": "₹120/kg", "Time Left": "10 min"},
        {"Fruit": "Banana (Robusta)", "Current Bid": "₹45/kg", "Time Left": "30 min"},
        {"Fruit": "Apple (Shimla)", "Current Bid": "₹150/kg", "Time Left": "5 min"},
    ],
    use_container_width=True,
)

st.markdown("---")
st.caption("📈 More analytics and charts coming soon!")
