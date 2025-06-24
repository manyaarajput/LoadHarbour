import threading
from core.logger import log_event  # ← added

db_lock = threading.Lock()

def save_file_to_db(filename, content, db):
    with db_lock:
        try:
            cursor = db.cursor()
            cursor.execute("INSERT INTO files (filename, content) VALUES (?, ?)", (filename, content))
            db.commit()
            log_event(operation="UPLOAD", filename=filename, status="SUCCESS")  # ← added
        except Exception as e:
            log_event(operation="UPLOAD", filename=filename, status="FAILURE", error=str(e))  # ← added
            raise

def get_all_files(db):
    with db_lock:
        cursor = db.cursor()
        cursor.execute("SELECT filename, content FROM files")
        return cursor.fetchall()

def get_file_by_name(filename, db):
    with db_lock:
        cursor = db.cursor()
        cursor.execute("SELECT filename, content FROM files WHERE filename = ?", (filename,))
        return cursor.fetchone()
