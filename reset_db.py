import sqlite3

print("🔄 Recreating 'users' table...")

# Connect to your database
conn = sqlite3.connect("fruitbid.db")
c = conn.cursor()

# Drop the table if it exists
c.execute("DROP TABLE IF EXISTS users")

# Create a clean version of the users table
c.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone TEXT UNIQUE,
        otp TEXT,
        verified INTEGER DEFAULT 0
    )
""")

conn.commit()
conn.close()

print("✅ Table 'users' recreated successfully with columns: id, phone, otp, verified")
