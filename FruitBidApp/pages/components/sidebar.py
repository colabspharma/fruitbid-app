import streamlit as st

def render_sidebar():
    """Render the main navigation sidebar for FruitBid."""
    with st.sidebar:
        st.title("🍉 FruitBid")
        st.markdown("### 🧭 Navigation")

        page = st.radio(
            "Go to:",
            [
                "🏠 Home",
                "🏪 Marketplace",
                "💼 My Bids",
                "⚙️ Add Lot (Admin)"
            ],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.caption("🌿 Supporting local farmers, one bid at a time.")

    return page
