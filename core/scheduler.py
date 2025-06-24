import threading
import time
from queue import PriorityQueue
from core.processor import process_file

workers = [threading.Semaphore(1) for _ in range(3)]  # Simulate 3 worker nodes

# Basic Round Robin Scheduler
def schedule_files(queue):
    i = 0
    while queue:
        filename, content, db = queue.pop(0)
        worker = workers[i % len(workers)]
        threading.Thread(target=process_file, args=(filename, content, db, worker), daemon=True).start()
        i += 1
        time.sleep(0.1)  

# Least Loaded Node Scheduler
def schedule_least_loaded(queue):
    while queue:
        worker = min(workers, key=lambda w: w._value)  # lowest semaphore count (more available)
        filename, content, db = queue.pop(0)
        threading.Thread(target=process_file, args=(filename, content, db, worker), daemon=True).start()
        time.sleep(0.1)

# Priority Based Scheduler using file size (or metadata)
def schedule_priority(queue):
    pq = PriorityQueue()
    for job in queue:
        filename, content, db = job
        pq.put((len(content), job))  
    while not pq.empty():
        _, (filename, content, db) = pq.get()
        worker = min(workers, key=lambda w: w._value)
        threading.Thread(target=process_file, args=(filename, content, db, worker), daemon=True).start()
        time.sleep(0.1)
