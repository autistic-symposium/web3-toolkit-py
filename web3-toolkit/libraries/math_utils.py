# -*- encoding: utf-8 -*-
# math_utils.py
# This class implements math methods used by the other classes.


import base64
import hashlib


def str_to_bytes(data):
    """Convert string to bytes."""
    utype = type(b''.decode('utf8'))

    if isinstance(data, utype):
        return data.encode('utf8')

    return data


def b64encode(data: str) -> str:
    """Encode data to base64."""
    return base64.b64encode(data).decode('utf-8')


def b64decode(data: str) -> str:
    """Decode base64 data."""
    return base64.b64decode(data)


def hash256(data: str) -> str:
    """Hash data with SHA-256."""
    return hashlib.sha256(str_to_bytes(data)).digest()
