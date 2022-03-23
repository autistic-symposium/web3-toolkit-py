#!/usr/bin/env python3

from multiprocessing import Pool


def f(x):
    return x*x


p = Pool(5)
print(p.map(f, [1, 2, 3]))