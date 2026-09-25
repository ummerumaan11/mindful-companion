import sqlite3
from datetime import datetime
from contextlib import contextmanager

DB_PATH = "companion.db"


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS mood_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                mood_score INTEGER NOT NULL,
                note TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                text TEXT NOT NULL
            )
        """)
        conn.commit()


def add_mood_entry(mood_score: int, note: str = ""):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO mood_entries (timestamp, mood_score, note) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), mood_score, note),
        )
        conn.commit()


def get_mood_history():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM mood_entries ORDER BY timestamp ASC").fetchall()
        return [dict(r) for r in rows]


def add_journal_entry(text: str):
    with get_conn() as conn:
        conn.execute(
            "INSERT INTO journal_entries (timestamp, text) VALUES (?, ?)",
            (datetime.now().isoformat(), text),
        )
        conn.commit()


def get_journal_entries():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM journal_entries ORDER BY timestamp DESC").fetchall()
        return [dict(r) for r in rows]
