import streamlit as st

def render_sidebar():
    """Reusable sidebar for all FruitBid pages."""
    with st.sidebar:
        st.title("🍇 FruitBid")
        st.markdown(f"**👤 {st.session_state.get('user_name', 'Guest')} ({st.session_state.get('phone', 'N/A')})**")
        st.markdown("---")

        # Navigation options
        menu = ["🏠 Home", "📊 Dashboard", "🏪 Marketplace", "💼 My Bids", "⚙️ Add Lot (Admin)"]
        choice = st.radio("Navigate to:", menu)

        st.markdown("---")

        # Logout button
        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.info("✅ You’ve been logged out successfully.")
            st.switch_page("app_web.py")

        st.markdown("---")
        st.caption("🌿 Powered by FruitBid")

    return choice
