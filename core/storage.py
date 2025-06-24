import threading
from core.logger import log_event  # ← added

db_lock = threading.Lock()

def save_file_to_db(filename, content, db):
    with db_lock:
        cursor = db.cursor()
        cursor.execute("INSERT INTO files (filename, content) VALUES (?, ?)", (filename, content))
        db.commit()

def get_all_files(db):
    with db_lock:
        cursor = db.cursor()
        cursor.execute("SELECT filename FROM files")
        return [row[0] for row in cursor.fetchall()]

def get_file_by_name(filename, db):
    with db_lock:
        cursor = db.cursor()
        cursor.execute("SELECT filename, content FROM files WHERE filename = ?", (filename,))
        result = cursor.fetchone()
        if result:
            name, content = result
            return name, content
        return None

def delete_file_by_name(filename, db):
    with db_lock:
        cursor = db.cursor()
        cursor.execute("DELETE FROM files WHERE filename = ?", (filename,))
        db.commit()
        deleted = cursor.rowcount
        if deleted:
            log_event(operation="DELETE", filename=filename, status="SUCCESS")  # ← added log
        else:
            log_event(operation="DELETE", filename=filename, status="FAILURE", error="File not found")  # ← added log
        return deleted
