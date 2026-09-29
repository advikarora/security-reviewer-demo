import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash

DB_PATH = Path(__file__).resolve().parent.parent / "demo.db"


def connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with connect() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                api_token TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'user'
            );
            DELETE FROM users;
            """
        )
        conn.executemany(
            "INSERT INTO users (id, username, password_hash, api_token, role) VALUES (?, ?, ?, ?, ?)",
            [
                (1, "alice", generate_password_hash("alice-password"), "alice-demo-token", "user"),
                (2, "bob", generate_password_hash("bob-password"), "bob-demo-token", "user"),
                (3, "admin", generate_password_hash("admin-password"), "admin-demo-token", "admin"),
            ],
        )


def get_user_by_username(username):
    # DEMO VULNERABILITY: user input is inserted directly into SQL.
    query = f"SELECT id, username, password_hash, api_token, role FROM users WHERE username = '{username}'"
    with connect() as conn:
        return conn.execute(query).fetchone()


def get_user_by_id(user_id):
    with connect() as conn:
        return conn.execute(
            "SELECT id, username, api_token, role FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
