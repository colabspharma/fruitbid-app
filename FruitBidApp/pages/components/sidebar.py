# FruitBidApp/components/sidebar.py

import streamlit as st

def render_sidebar():
    st.sidebar.title("🍉 FruitBid Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["🏠 Home", "🍇 Dashboard", "💼 My Bids", "📊 Reports", "⚙️ Settings"]
    )
    st.sidebar.write("Select a page to view.")
    return page
