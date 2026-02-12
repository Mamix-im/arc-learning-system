import sqlite3


def init_db():

    conn = sqlite3.connect("arc.db")
    cur = conn.cursor()

    # Learning Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS learning (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        status TEXT,
        note TEXT,
        date TEXT
    )
    """)

    # Game Score Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        score INTEGER,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database Ready")
