import sqlite3
from threading import Lock
import os

db_lock = Lock()

DB_FILE = "files.db"

def get_db_session():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                content BLOB
            )
        ''')
        conn.commit()
        conn.close()
