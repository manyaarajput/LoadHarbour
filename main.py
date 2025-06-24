from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List
import threading
import io

from core.scheduler import schedule_files, schedule_least_loaded, schedule_priority
from db.database import get_db_session, init_db
from core.storage import get_all_files, get_file_by_name, delete_file_by_name  # updated import

app = FastAPI(title="Load Harbour - File Processing Hub")

# Initialize database and ensure table exists
init_db()

# Thread-safe job queue and lock
job_queue = []
queue_lock = threading.Lock()

# Choose scheduler here
scheduler = schedule_files  # can switch to schedule_least_loaded or schedule_priority

def background_scheduler():
    while True:
        with queue_lock:
            if job_queue:
                scheduler(job_queue)
        # Sleep a bit to prevent busy waiting
        threading.Event().wait(1)

# Start background thread once at startup
threading.Thread(target=background_scheduler, daemon=True).start()

@app.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    db = get_db_session()
    for file in files:
        contents = await file.read()
        with queue_lock:
            job_queue.append((file.filename, contents, db))
    return {"message": "Files uploaded and scheduled for processing."}

@app.get("/")
def read_root():
    return {"message": "Welcome to Load Harbour - A stable and efficient file processing hub"}

@app.get("/files/")
def list_files():
    db = get_db_session()
    files = get_all_files(db)
    return {"files": files}

@app.get("/files/{filename}")
def download_file(filename: str):
    db = get_db_session()
    file_record = get_file_by_name(filename, db)
    if file_record is None:
        raise HTTPException(status_code=404, detail="File not found")

    content = file_record[1]
    # If content is string, encode it to bytes
    if isinstance(content, str):
        content = content.encode('utf-8')

    return StreamingResponse(io.BytesIO(content), media_type="application/octet-stream", headers={
        "Content-Disposition": f"attachment; filename={filename}"
    })

@app.delete("/files/{filename}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(filename: str):
    db = get_db_session()
    deleted_count = delete_file_by_name(filename, db)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": f"File '{filename}' deleted successfully."}
