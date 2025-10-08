# =====================================================
# 🛠️ FruitBid Admin Dashboard
# =====================================================

import streamlit as st
import sqlite3
from contextlib import closing

# Try importing DB helpers safely
try:
    from db import init_db, initialize_items, get_db_connection
except ImportError:
    st.error("⚠️ Missing `db.py` module. Please ensure it exists in your project folder.")
    st.stop()

# =====================================================
# ⚙️ PAGE SETUP
# =====================================================

st.title("🛠️ FruitBid Admin Dashboard")
st.markdown("Manage your database and system configuration safely below.")
st.markdown("---")


# =====================================================
# 🔄 DATABASE RESET (Admin Tools)
# =====================================================
st.subheader("⚙️ Database Management")

col1, col2 = st.columns(2)

with col1:
    if st.button("🧹 Reset Database (Delete Everything)"):
        with st.spinner("Deleting old database and creating a new one..."):
            try:
                reset_database()
                init_db()
                initialize_items()
                st.success("✅ Database fully reset and re-seeded with demo data!")
                st.balloons()
            except Exception as e:
                st.error(f"❌ Database reset failed:\n\n{e}")

with col2:
    if st.button("🔄 Reinitialize Sample Items"):
        with st.spinner("Adding or refreshing fruit lots..."):
            try:
                initialize_items()
                st.success("✅ Sample fruit lots initialized successfully!")
            except Exception as e:
                st.error(f"❌ Initialization failed:\n\n{e}")



# =====================================================
# 📊 DATABASE OVERVIEW
# =====================================================
st.subheader("📊 Database Overview")

TABLES = [
    "users",
    "items",
    "bids",
    "settings",
    "otps",
    "nutrition",
    "lucky_dip",
]

summary_data = []

try:
    with closing(get_db_connection()) as conn:
        if conn is None:
            raise RuntimeError("Database connection could not be established.")
        with closing(conn.cursor()) as c:
            for table in TABLES:
                try:
                    c.execute(f"SELECT COUNT(*) FROM {table}")
                    count = c.fetchone()[0]
                    summary_data.append({"Table": table, "Records": count})
                except sqlite3.OperationalError:
                    summary_data.append({"Table": table, "Records": "❌ Not Found"})
                except Exception as e:
                    summary_data.append({"Table": table, "Records": f"⚠️ {type(e).__name__}"})

    st.write("### Table Summary")
    st.dataframe(summary_data, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Database access error: {e}")

# =====================================================
# 🧾 RAW DB INSPECTION (Optional)
# =====================================================
with st.expander("🧾 Inspect Table Contents"):
    selected_table = st.selectbox("Select a table to view its records:", TABLES)
    if st.button("View Table"):
        try:
            with closing(get_db_connection()) as conn:
                if conn:
                    with closing(conn.cursor()) as c:
                        c.execute(f"PRAGMA table_info({selected_table})")
                        columns = [col[1] for col in c.fetchall()]
                        c.execute(f"SELECT * FROM {selected_table} LIMIT 20")
                        rows = c.fetchall()
                        if rows:
                            st.dataframe(
                                [dict(zip(columns, row)) for row in rows],
                                use_container_width=True,
                            )
                        else:
                            st.info("No records found in this table.")
        except Exception as e:
            st.error(f"❌ Failed to read table `{selected_table}`:\n\n{e}")

# =====================================================
# 🧩 FOOTER
# =====================================================
st.markdown("---")
st.caption("🧑‍💼 FruitBid Admin v1.0 • Use responsibly 💡")
