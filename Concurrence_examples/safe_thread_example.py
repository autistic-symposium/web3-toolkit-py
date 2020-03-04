#!/usr/bin/env python3

import threading

counter = 0
threads = []

lock = threading.Lock()


def count_with_lock():

    global counter

    for _ in range(100):
        with lock:
            counter += 1


for _ in range(100):
    thread = threading.Thread(target=count_with_lock)
    thread.start()
    threads.append(thread)


print(counter)