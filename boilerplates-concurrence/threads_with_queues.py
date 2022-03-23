from queue import Queue
from threading import Thread


NUM_WORKERS = 4
task_queue = Queue()


def worker():
    while True:
        address = task_queue.get()
        run_function(address)
        task_queue.task_done()


threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]
[task_queue.put(item) for item in threads]
[thread.start() for thread in threads]
task_queue.join()