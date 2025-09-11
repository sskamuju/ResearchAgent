


import sqlite3
import json

DB_PATH = "agent_memory.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_query TEXT,
            plan_json TEXT,
            output_md TEXT
        );
    """)
    conn.commit()
    conn.close()

def save_run(user_query: str, plan: dict, output_md: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO runs (user_query, plan_json, output_md) VALUES (?, ?, ?)",
        (user_query, json.dumps(plan), output_md)
    )
    conn.commit()
    conn.close()

def get_all_runs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT id, user_query FROM runs ORDER BY id DESC")
    runs = cursor.fetchall()
    conn.close()
    return runs

def get_run_details(run_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT * FROM runs WHERE id = ?", (run_id,))
    row = cursor.fetchone()
    conn.close()
    return row
