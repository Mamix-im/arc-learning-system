import sqlite3

# Database connect karo (file create hogi)
conn = sqlite3.connect("arc.db")

# Cursor = command dene ka tool
cur = conn.cursor()

# Table banana
cur.execute("""
CREATE TABLE IF NOT EXISTS learning (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    status TEXT,
    note TEXT,
    date TEXT
)
""")

# Save changes
conn.commit()

# Close connection
conn.close()

print("Learning Database Ready")
