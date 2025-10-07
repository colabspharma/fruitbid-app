# =====================================================
# 🍇 components/sidebar.py — Reusable Sidebar Component
# =====================================================

import streamlit as st

def render_sidebar(page_id: str = "default"):
    """
    Reusable, crash-proof sidebar for all FruitBid pages.
    'page_id' ensures unique widget keys (fixes DuplicateWidgetID).
    Defaults to 'default' for backward compatibility.
    """

    with st.sidebar:
        # =====================================================
        # 🍉 Header Section
        # =====================================================
        st.title("🍇 FruitBid")

        user_name = st.session_state.get("user_name", "Guest")
        user_phone = st.session_state.get("phone", "N/A")

        st.markdown(f"**👤 {user_name} ({user_phone})**")
        st.markdown("---")

        # =====================================================
        # 🧭 Navigation Menu
        # =====================================================
        menu = [
            "🏠 Home",
            "📊 Dashboard",
            "🏪 Marketplace",
            "💼 My Bids",
            "⚙️ Add Lot (Admin)",
            "🛠️ System"
        ]

        # ✅ Unique key per page — prevents DuplicateWidgetID
        choice = st.radio(
            "Navigate to:",
            menu,
            label_visibility="collapsed",
            key=f"sidebar_nav_{page_id}"
        )

        st.markdown("---")

        # =====================================================
        # 🚪 Logout Button
        # =====================================================
        if st.button("🚪 Logout", use_container_width=True, key=f"logout_{page_id}"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.success("✅ Logged out successfully.")
            st.rerun()

        # =====================================================
        # 📋 Footer
        # =====================================================
        st.markdown("---")
        st.caption("🌿 Powered by FruitBid • v1.0")

    return choice
