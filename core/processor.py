import time
import threading
from core.storage import save_file_to_db
from core.logger import log_event  # ← added

MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

def process_file(filename, content, db, worker):
    with worker:
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                print(f"[Processing] {filename} (Attempt {attempt})")
                time.sleep(2)  # Simulate I/O delay
                save_file_to_db(filename, content, db)
                print(f"[Saved] {filename}")
                log_event(operation="UPLOAD", filename=filename, status="SUCCESS")  # ← added log
                break  # ✅ Success: exit loop
            except Exception as e:
                print(f"[Error] {filename} failed on attempt {attempt}: {e}")
                if attempt < MAX_RETRIES:
                    print(f"[Retrying] {filename} in {RETRY_DELAY} seconds...")
                    time.sleep(RETRY_DELAY)
                else:
                    print(f"[Failed Permanently] {filename} after {MAX_RETRIES} attempts.")
                    log_event(operation="UPLOAD", filename=filename, status="FAILURE", error=str(e))  # ← added log
