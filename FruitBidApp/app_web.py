# =====================================================
# 🍎 app_web.py — Main FruitBid App Entry Point (fixed)
# =====================================================

import os
import sqlite3
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components

# =====================================================
# ✅ PAGE CONFIG
# =====================================================
if "page_configured" not in st.session_state:
    try:
        st.set_page_config(
            page_title="🍎 FruitBid App",
            page_icon="🍇",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        st.session_state["page_configured"] = True
    except st.errors.StreamlitAPIException:
        pass


# =====================================================
# 🍉 BACKGROUND (CSS injected into Streamlit root)
# =====================================================
st.markdown(
    """
    <style>
    /* apply soft green gradient to Streamlit app root */
    .stApp {
        background: linear-gradient(180deg, #f3fff3, #d6ffd6);
        min-height: 100vh;
        overflow: hidden;
    }

    /* keep normal content above visuals */
    .main > div {
        background: transparent !important;
    }

    /* button / input styling kept consistent with theme */
    div.stButton > button {
      background: linear-gradient(90deg, #26a69a, #80cbc4);
      color: white;
      border: none;
      border-radius: 12px;
      padding: 0.6rem 1.2rem;
      font-weight: 600;
      transition: all 0.3s ease-in-out;
      box-shadow: 0px 3px 10px rgba(38, 166, 154, 0.4);
    }
    div.stButton > button:hover {
      background: linear-gradient(90deg, #00796b, #4db6ac);
      transform: translateY(-2px);
      box-shadow: 0px 6px 12px rgba(0, 121, 107, 0.3);
    }

    input, textarea, select {
      border-radius: 8px !important;
      border: 1px solid #b2dfdb !important;
      background-color: #ffffff !important;
      color: #004d40 !important;
    }
    input:focus, textarea:focus, select:focus {
      border: 1px solid #26a69a !important;
      box-shadow: 0 0 0 3px rgba(38, 166, 154, 0.2) !important;
      outline: none !important;
    }

    h2, h3 {
      color: #00695c !important;
      font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# 🍉 Floating fruits animation (runs in an invisible iframe)
# =====================================================
# This uses components.html() with height=0 so JS executes reliably.
components.html(
    """
    <!doctype html>
    <html>
      <head>
        <meta charset="utf-8" />
        <style>
          /* minimal styles inside iframe - fruits spawn and remove themselves */
          body { margin:0; padding:0; overflow: hidden; background: transparent; }
          .fruit {
            position: fixed;
            bottom: -10vh;
            font-size: 2.2rem;
            opacity: 0.9;
            animation: floatUp linear infinite;
            user-select: none;
            pointer-events: none;
            z-index: 0;
          }
          @keyframes floatUp {
            0% { transform: translateY(0) translateX(0) rotate(0deg); opacity: 0.9; }
            50% { transform: translateY(-50vh) translateX(3vw) rotate(10deg); opacity: 1; }
            100% { transform: translateY(-110vh) translateX(-3vw) rotate(-10deg); opacity: 0; }
          }
        </style>
      </head>
      <body>
        <div id="__fruit_root"></div>
        <script>
          (function() {
            const fruits = ["🍎","🍊","🍋","🍇","🍌","🍉","🍒","🍓","🍍","🥭"];
            const root = document.getElementById("__fruit_root");

            function spawnFruit() {
              const el = document.createElement("div");
              el.className = "fruit";
              el.textContent = fruits[Math.floor(Math.random() * fruits.length)];
              el.style.left = (Math.random() * 100) + "vw";
              el.style.fontSize = (1.3 + Math.random() * 1.4) + "rem";
              el.style.animationDuration = (7 + Math.random() * 6) + "s";
              el.style.animationDelay = (Math.random() * 2) + "s";
              root.appendChild(el);
              setTimeout(() => {
                try { root.removeChild(el); } catch (e) {}
              }, 15000);
            }

            // initial burst then periodic spawn
            for (let i = 0; i < 16; i++) spawnFruit();
            setInterval(spawnFruit, 1200);
          })();
        </script>
      </body>
    </html>
    """,
    height=0,
    width=0,
)


# =====================================================
# 📂 SIDEBAR (import or fallback)
# =====================================================
try:
    from components.sidebar import render_sidebar
except ModuleNotFoundError:
    def render_sidebar():
        with st.sidebar:
            return st.radio(
                "Navigate:",
                ["🏠 Home", "🏪 Marketplace", "💼 My Bids", "⚙️ Add Lot (Admin)"]
            )
    st.warning("⚠️ Sidebar missing — using fallback menu.")


# =====================================================
# 🗄️ DATABASE HELPERS
# =====================================================
DB_PATH = os.path.join("/app", "fruitbid.db")

def get_connection():
    """Return a sqlite3 connection (threads allowed)."""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            verified INTEGER DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS lots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT,
            quantity TEXT,
            base_price REAL,
            date_added TEXT
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS bids (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            lot_id INTEGER,
            bid_amount REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def seed_data():
    """Seed demo lots only when table is empty."""
    conn = get_connection()
    c = conn.cursor()
    try:
        c.execute("SELECT COUNT(*) FROM lots")
        count = c.fetchone()[0]
    except sqlite3.OperationalError:
        # If schema not present, create it and treat as empty
        count = 0

    if count == 0:
        st.info("🌱 Seeding sample fruit lots...")
        sample_lots = [
            ("Apples", "100 kg", 120.0, datetime.now().strftime("%Y-%m-%d")),
            ("Bananas", "200 kg", 60.0, datetime.now().strftime("%Y-%m-%d")),
            ("Mangoes", "150 kg", 180.0, datetime.now().strftime("%Y-%m-%d")),
            ("Oranges", "180 kg", 90.0, datetime.now().strftime("%Y-%m-%d")),
        ]
        try:
            c.executemany(
                "INSERT INTO lots (item_name, quantity, base_price, date_added) VALUES (?, ?, ?, ?)",
                sample_lots
            )
            conn.commit()
        except sqlite3.OperationalError as e:
            st.error(f"❌ Database insert failed: {e}")
    conn.close()

def execute_query(query, params=()):
    conn = get_connection()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()

def fetch_all(query, params=()):
    conn = get_connection()
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows
# =====================================================
# 🗄️ DATABASE HELPERS (Streamlit Cloud Safe)
# =====================================================
DB_PATH = os.path.join("/app", "fruitbid.db")

def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


# =====================================================
# 🌐 MAIN APP FUNCTION
# =====================================================
def main():
    init_db()
    seed_data()

    st.title("🍎 FruitBid — Fresh Produce, Fast Deals")
    selected_page = render_sidebar()

    # --------------------------
    # 🏠 HOME
    # --------------------------
    if selected_page == "🏠 Home":
        st.subheader("👋 Welcome to FruitBid")
        st.info("OTP login temporarily disabled for testing.")

        name = st.text_input("Your Name")
        phone = st.text_input("Phone Number (optional)")

        if st.button("Enter Marketplace"):
            if not name or not name.strip():
                st.warning("Please enter your name.")
            else:
                st.session_state["user_name"] = name.strip()
                st.session_state["phone"] = phone.strip()
                st.success(f"Welcome, {name.strip()}! Use the sidebar to explore the Marketplace.")

    # --------------------------
    # 🏪 MARKETPLACE
    # --------------------------
    elif selected_page == "🏪 Marketplace":
        st.subheader("🏪 Marketplace — Active Lots")
        lots = fetch_all(
            "SELECT id, item_name, quantity, base_price, date_added FROM lots ORDER BY id DESC"
        )

        if not lots:
            st.warning("No lots available yet.")
        else:
            for lot_id, item_name, quantity, base_price, date_added in lots:
                with st.expander(f"{item_name} ({quantity}) — Base ₹{base_price}"):
                    st.write(f"📅 Added: {date_added}")
                    bid_amount = st.number_input(
                        f"Enter your bid for {item_name} (₹)",
                        min_value=float(base_price),
                        key=f"bid_{lot_id}"
                    )
                    if st.button(f"💰 Submit Bid for {item_name}", key=f"submit_{lot_id}"):
                        user_name = st.session_state.get("user_name", "Guest")
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        execute_query(
                            "INSERT INTO bids (user_name, lot_id, bid_amount, timestamp) VALUES (?, ?, ?, ?)",
                            (user_name, lot_id, bid_amount, timestamp)
                        )
                        st.success(f"✅ ₹{bid_amount} bid placed on {item_name}!")

                    top_bids = fetch_all(
                        "SELECT user_name, bid_amount, timestamp FROM bids WHERE lot_id = ? ORDER BY bid_amount DESC LIMIT 3",
                        (lot_id,)
                    )
                    if top_bids:
                        st.write("📊 Top Bids:")
                        for user, amount, ts in top_bids:
                            st.write(f"• {user} — ₹{amount} ({ts})")

    # --------------------------
    # 💼 MY BIDS
    # --------------------------
    elif selected_page == "💼 My Bids":
        st.subheader("💼 My Bids")
        user_name = st.session_state.get("user_name")
        if not user_name:
            st.warning("Please enter your name on the Home page first.")
        else:
            my_bids = fetch_all(
                """
                SELECT lots.item_name, bids.bid_amount, bids.timestamp
                FROM bids
                JOIN lots ON bids.lot_id = lots.id
                WHERE bids.user_name = ?
                ORDER BY bids.timestamp DESC
                """,
                (user_name,)
            )
            if not my_bids:
                st.info("No bids placed yet.")
            else:
                for item, amount, ts in my_bids:
                    st.write(f"🍇 {item} — ₹{amount} at {ts}")

    # --------------------------
    # ⚙️ ADMIN
    # --------------------------
    elif selected_page == "⚙️ Add Lot (Admin)":
        st.subheader("⚙️ Admin: Add a New Lot")
        item_name = st.text_input("Fruit Name")
        quantity = st.text_input("Quantity (e.g. 10 kg, 1 box)")
        base_price = st.number_input("Base Price (₹)", min_value=1.0, step=0.5)

        if st.button("Add Lot"):
            if item_name and quantity:
                execute_query(
                    "INSERT INTO lots (item_name, quantity, base_price, date_added) VALUES (?, ?, ?, ?)",
                    (item_name, quantity, base_price, datetime.now().strftime("%Y-%m-%d"))
                )
                st.success(f"✅ Added new lot: {item_name} ({quantity}) at ₹{base_price}")
            else:
                st.warning("Please fill in all fields.")


# =====================================================
# 🚀 RUN
# =====================================================
if __name__ == "__main__":
    main()


# =====================================================
# 🍎 FOOTER
# =====================================================
st.markdown(
    """
    <hr style='margin-top:2rem; opacity:0.3;'>
    <p style='text-align:center; color:#00695c; font-size:0.9rem;'>
    Built with ❤️ using Streamlit — <b>FruitBid App</b>
    </p>
    """,
    unsafe_allow_html=True,
)
