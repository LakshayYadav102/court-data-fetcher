import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("court_data.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            case_type TEXT,
            case_number TEXT,
            case_year TEXT,
            raw_html TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_query(case_type, case_number, case_year, raw_html):
    conn = sqlite3.connect("court_data.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO queries (timestamp, case_type, case_number, case_year, raw_html)
        VALUES (?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), case_type, case_number, case_year, raw_html))
    conn.commit()
    conn.close()
