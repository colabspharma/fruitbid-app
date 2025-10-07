import streamlit as st
import sqlite3
from db import init_db, initialize_items, get_db_connection

st.set_page_config(page_title="Admin Dashboard", page_icon="🛠️", layout="wide")

st.title("🛠️ Admin Dashboard")
st.markdown("Manage your FruitBid database and app settings here.")

# --------------------------
# Reset Database Button
# --------------------------
st.subheader("⚙️ Database Management")

if st.button("🔄 Reset Database (Recreate Tables & Items)", type="primary"):
    with st.spinner("Reinitializing database..."):
        try:
            init_db()
            initialize_items()
            st.success("✅ Database has been reinitialized successfully!")
        except Exception as e:
            st.error(f"❌ Failed to reinitialize database: {str(e)}")


# --------------------------
# Database Overview Section
# --------------------------
st.subheader("📊 Database Overview")

try:
    conn = get_db_connection()
    c = conn.cursor()

    tables = ["users", "items", "bids", "settings", "otps", "nutrition", "lucky_dip"]
    data_summary = {}

    for table in tables:
        try:
            c.execute(f"SELECT COUNT(*) FROM {table}")
            count = c.fetchone()[0]
            data_summary[table] = count
        except sqlite3.Error:
            data_summary[table] = "❌ Not Found"

    st.write("### Table Summary:")
    st.dataframe(
        [{"Table": t, "Records": data_summary[t]} for t in data_summary],
        use_container_width=True
    )

except Exception as e:
    st.error(f"⚠️ Error connecting to database: {str(e)}")


# --------------------------
# Footer
# --------------------------
st.markdown("---")
st.caption("FruitBid Admin • v1.0 | Use responsibly 💡")
