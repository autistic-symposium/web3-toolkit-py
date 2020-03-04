#!/usr/bin/env python3

import threading

x = 0     

COUNT = 10000000

def foo():
    global x
    for i in xrange(COUNT):
        x += 1

def bar():
    global x
    for i in xrange(COUNT):
        x -= 1

t1 = threading.Thread(target=foo)
t2 = threading.Thread(target=bar)

t1.start()
t2.start()

t1.join()
t2.join()

print(x)
