import sqlite3
from datetime import datetime

DB_NAME = "data.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTERGER PRIMARY KEY,
                username TEXT,
                created_at TEXT          
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                text TEXT,
                status TEXT DEFAULT 'active',
                created_at TEXT,
                done_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        """)
        conn.commit()

def add_user(user_id, username):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR IGNORE INTO users (user_id, username, created_at) VALUES (?, ?, ?)",
            (user_id, username, datetime.now().isoformat())
        )
        conn.commit()

def add_task(user_id, text):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (user_id, text, created_at, status) VALUES (?, ?, ?, ?)",
            (user_id, text, datetime.now().isoformat(), 'active')
        )
        conn.commit()
        return cursor.lastrowid

def get_active_tasks(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, text, created_at FROM tasks WHERE user_id = ? AND status = 'active' ORDER BY created_at",
            (user_id,)
        )
        return cursor.fetchall()

def get_all_tasks(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, text, status, created_at, done_at FROM tasks WHERE user_id = ? ORDER BY created_at DESC",
            (user_id,)
        )
        return cursor.fetchall()

def mark_task_done(task_id, user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = 'done', done_at = ? WHERE id = ? AND user_id = ? AND status = 'active'",
            (datetime.now().isoformat(), task_id, user_id)
        )
        conn.commit()
        return cursor.rowcount > 0

def get_stats(user_id):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE user_id = ?",
            (user_id,)
        )
        total = cursor.fetchone()[0]
        
        cursor.execute(
            "SELECT COUNT(*) FROM tasks WHERE user_id = ? AND status = 'active'",
            (user_id,)
        )
        active = cursor.fetchone()[0]
        
        done = total - active
        return total, active, done