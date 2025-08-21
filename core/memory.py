


import sqlite3
from datetime import datetime
import json
from pathlib import Path

DB_PATH = Path("memory.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_prompt TEXT,
                timestamp TEXT,
                plan_json TEXT,
                results_json TEXT,
                synthesized TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS citations (
                url TEXT PRIMARY KEY,
                citation_id INTEGER
            )
        ''')
        conn.commit()

def save_interaction(prompt, plan, results, synthesized):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO interactions (user_prompt, timestamp, plan_json, results_json, synthesized)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            prompt,
            datetime.now().isoformat(),
            json.dumps(plan.model_dump()),
            json.dumps(results),
            synthesized
        ))
        conn.commit()

def get_or_create_citation_id(url):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT citation_id FROM citations WHERE url = ?", (url,))
        row = cursor.fetchone()
        if row:
            return row[0]
        else:
            cursor.execute("SELECT MAX(citation_id) FROM citations")
            max_id = cursor.fetchone()[0]
            new_id = 1 if max_id is None else max_id + 1
            cursor.execute("INSERT INTO citations (url, citation_id) VALUES (?, ?)", (url, new_id))
            conn.commit()
            return new_id

def get_all_citations():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT url, citation_id FROM citations")
        return dict(cursor.fetchall())

