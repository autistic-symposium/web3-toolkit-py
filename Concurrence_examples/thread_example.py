import time
import random
import threading


def worker(n):
    sleep = random.randrange(1, 10)
    time.sleep(sleep)
    print("Worker {}: sleeping for {} seconds.".format(n, sleep))


for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
