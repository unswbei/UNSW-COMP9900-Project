#!/usr/bin/python3

import hashlib

def sha256(hash_string):
    """sha256 hash encrypt
    Param:
    hash_string -- string to encrypt
    Return:
    hex digest of encrypted string
    """
    m = hashlib.sha256()
    m.update(hash_string.encode())
    return m.hexdigest()
