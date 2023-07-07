# -*- encoding: utf-8 -*-
# utils/strings.py
# This class implements string methods used by the other classes.

from pprint import PrettyPrinter

def pprint(data, indent=None) -> None:
    """Print dicts and data in a suitable format"""

    print()
    indent = indent or 4
    pp = PrettyPrinter(indent=indent)
    pp.pprint(data)
    print()
