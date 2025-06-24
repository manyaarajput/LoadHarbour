import os
from datetime import datetime

LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "events.log")

# Make sure log folder exists
os.makedirs(LOG_DIR, exist_ok=True)

def log_event(operation, filename, status, error=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {operation.upper()} | {filename} | {status}"
    if error:
        log_line += f" | ERROR: {error}"
    log_line += "\n"

    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_line)
