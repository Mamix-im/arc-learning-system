import sqlite3


def init_db():

    conn = sqlite3.connect("arc.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS learning (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT,
        status TEXT,
        note TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully!")
