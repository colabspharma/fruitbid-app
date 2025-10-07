import streamlit as st

# 🧩 Page setup
st.set_page_config(page_title="Marketplace", page_icon="🏪", layout="wide")

# 🔒 Login guard
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

# 🏪 Marketplace Content
st.title("🏪 Marketplace")
st.write("Browse and bid on the freshest fruit lots!")

# 📦 Example mock data
lots = [
    {"Fruit": "Mango (Alphonso)", "Base Price": "₹120/kg", "Highest Bid": "₹135/kg", "Time Left": "10 min"},
    {"Fruit": "Banana (Robusta)", "Base Price": "₹45/kg", "Highest Bid": "₹48/kg", "Time Left": "30 min"},
    {"Fruit": "Apple (Shimla)", "Base Price": "₹150/kg", "Highest Bid": "₹158/kg", "Time Left": "5 min"},
]

st.dataframe(lots, use_container_width=True)

st.markdown("---")

# 💰 Bidding Interface
selected = st.selectbox("Select a fruit to bid on", [l["Fruit"] for l in lots])
bid = st.number_input("Enter your bid (₹/kg)", min_value=1, step=1)

if st.button("💰 Place Bid"):
    st.success(f"✅ Your bid of ₹{bid}/kg for **{selected}** has been recorded!")
