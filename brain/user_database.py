import sqlite3
import uuid
from datetime import datetime, timezone

DB = "data/nitron_users.db"


def get_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT,
            created_at TEXT NOT NULL,
            last_seen TEXT NOT NULL,
            messages INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    return conn


def register_user(username="User"):
    conn = get_db()

    now = datetime.now(timezone.utc).isoformat()
    user_id = str(uuid.uuid4())

    conn.execute(
        "INSERT INTO users (id, username, created_at, last_seen) VALUES (?, ?, ?, ?)",
        (user_id, username, now, now)
    )

    conn.commit()
    conn.close()

    return user_id


def record_message(user_id):
    conn = get_db()

    now = datetime.now(timezone.utc).isoformat()

    conn.execute("""
        UPDATE users
        SET last_seen = ?, messages = messages + 1
        WHERE id = ?
    """, (now, user_id))

    conn.commit()
    conn.close()


def total_users():
    conn = get_db()
    result = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    return result


def active_users_today():
    conn = get_db()

    today = datetime.now(timezone.utc).date().isoformat()

    result = conn.execute(
        "SELECT COUNT(*) FROM users WHERE last_seen LIKE ?",
        (today + "%",)
    ).fetchone()[0]

    conn.close()
    return result


def user_exists(user_id):
    conn = get_db()

    result = conn.execute(
        "SELECT 1 FROM users WHERE id = ? LIMIT 1",
        (user_id,)
    ).fetchone()

    conn.close()

    return result is not None
