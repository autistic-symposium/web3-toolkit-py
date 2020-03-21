#!/usr/bin/env python3

from time import sleep
from concurrent.futures import ThreadPoolExecutor


def return_after_5_secs(message):
    sleep(5)
    return message


pool = ThreadPoolExecutor(3)
future = pool.submit(return_after_5_secs, ('Future message'))

print(future.done())

sleep(5)
print(future.done())
print(future.result())