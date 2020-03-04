#!/usr/bin/env python3

import time
import threading

counter = 0
threads = []

def count():
    global counter
    for _ in range(100):
        counter += 1

for _ in range(100):
    thread = threading.Thread(target=count)
    thread.start()
    threads.append(thread)
 
for thread in threads:
    thread.join()

print(f"Count: {counter}")