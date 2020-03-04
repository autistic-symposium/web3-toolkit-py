#!/usr/bin/env python3

import time
import sys
import multiprocessing


def daemon():
    p = multiprocessing.current_process()

    print('Starting: {}, {}'.format(p.name, p.pid))
    sys.stdout.flush()
    time.sleep(2)
    print('Exiting : {}, {}'.format(p.name, p.pid))

    sys.stdout.flush()


def non_daemon():
    p = multiprocessing.current_process()

    print('Starting: {}, {}'.format(p.name, p.pid))
    sys.stdout.flush()
    print('Exiting : {}, {}'.format(p.name, p.pid))

    sys.stdout.flush()



if __name__ == '__main__':
    d = multiprocessing.Process(name='daemon', target=daemon)
    d.daemon = True

    n = multiprocessing.Process(name='non-daemon', target=non_daemon)
    n.daemon = False

    d.start()
    time.sleep(1)
    n.start()
