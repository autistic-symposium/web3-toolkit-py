#!/usr/bin/env python3

import time
import random
import threading


def worker(n):
    sleep = random.randrange(1, 10)
    time.sleep(sleep)
    print("Worker {} from {}: sleeping for {} seconds.".format(n, threading.get_ident(), sleep))


for i in range(5):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
