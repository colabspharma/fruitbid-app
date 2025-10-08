# db.py
import sqlite3
from datetime import datetime
import time

DB_PATH = "fruitbid.db"

# --------------------------
# Safe Connection Handler
# --------------------------
def get_db_connection(retries=3, delay=0.2):
    """Get SQLite connection with retry for busy DB."""
    for _ in range(retries):
        try:
            conn = sqlite3.connect(DB_PATH, timeout=5, check_same_thread=False)
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.OperationalError as e:
            if "database is locked" in str(e):
                time.sleep(delay)
            else:
                raise
    raise Exception("Database connection failed after retries")

# --------------------------
# Schema Initialization
# --------------------------
def init_db():
    """Create all required tables if they don't exist."""
    conn = get_db_connection()
    c = conn.cursor()

    try:
        c.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT UNIQUE
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS lots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                quantity TEXT,
                base_price REAL NOT NULL,
                date_added TEXT
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS bids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                lot_id INTEGER NOT NULL,
                bid_amount REAL NOT NULL,
                timestamp TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (lot_id) REFERENCES lots(id) ON DELETE CASCADE
            )
        """)

        # Optional meta table for version tracking
        c.execute("""
            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error creating tables: {str(e)}")
    finally:
        conn.close()

# --------------------------
# Insert Sample Lots
# --------------------------
def initialize_items():
    """Insert sample lots if table is empty."""
    conn = get_db_connection()
    c = conn.cursor()

    try:
        c.execute("SELECT COUNT(*) FROM lots")
        count = c.fetchone()[0]

        if count == 0:
            now = datetime.now().strftime("%Y-%m-%d %H:%M")
            sample_data = [
                ("Mango", "10 kg", 50, now),
                ("Banana", "20 kg", 30, now),
                ("Papaya", "15 kg", 40, now),
            ]
            c.executemany(
                """
                INSERT INTO lots (item_name, quantity, base_price, date_added)
                VALUES (?, ?, ?, ?)
                """,
                sample_data
            )
            conn.commit()
    except Exception as e:
        conn.rollback()
        raise Exception(f"Error inserting items: {str(e)}")
    finally:
        conn.close()

# --------------------------
# Utility for Clean Queries
# --------------------------
def fetch_all(query, params=()):
    """Fetch multiple rows safely."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return rows

def execute_query(query, params=()):
    """Execute INSERT/UPDATE safely."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute(query, params)
    conn.commit()
    conn.close()
