import streamlit as st

# 🧩 Page setup
st.set_page_config(page_title="My Bids", page_icon="💼", layout="wide")

# 🔒 Login Guard
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("⚠️ Please log in first from the main page.")
    st.stop()

# 🧭 Sidebar Navigation
st.sidebar.title("🍇 FruitBid")
st.sidebar.markdown(f"**👤 {st.session_state.phone}**")
st.sidebar.markdown("---")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.otp_sent = False
    st.session_state.phone = ""
    st.info("You’ve been logged out successfully.")
    st.switch_page("app_web.py")

# 🌟 Page Content
st.title("💼 My Bids")
st.write("Track your ongoing and past bids below:")
st.markdown("---")

# 📊 Example bid data
bids = [
    {"Fruit": "Mango (Alphonso)", "Your Bid": "₹135/kg", "Highest Bid": "₹135/kg", "Status": "🏆 Winning"},
    {"Fruit": "Banana (Robusta)", "Your Bid": "₹47/kg", "Highest Bid": "₹48/kg", "Status": "❌ Outbid"},
    {"Fruit": "Apple (Shimla)", "Your Bid": "₹158/kg", "Highest Bid": "₹158/kg", "Status": "🏆 Winning"},
]

st.dataframe(bids, use_container_width=True)

st.markdown("---")
st.caption("📊 Real-time bidding history and notifications coming soon!")
