#!/usr/bin/env python3

import threading 

l = threading.Lock()
print("Before first lock acquire.")

l.acquire()
print("Before second lock acquire.")

l.acquire()
print("Lock was acquired twice")
