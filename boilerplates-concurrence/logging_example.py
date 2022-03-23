#!/usr/bin/env python3

import sys
import logging
import multiprocessing


def worker():
    print('Doing some work...')
    sys.stdout.flush()


multiprocessing.log_to_stderr(logging.DEBUG)
p = multiprocessing.Process(target=worker)
p.start()
p.join()