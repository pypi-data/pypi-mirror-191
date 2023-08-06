# -*- coding: utf-8 -*-

"""Hash module.

This module provides the hash features for password creation and
secret key validation.
"""

from hashlib import new
from uuid import uuid4
from json import load, dump

from pashword.core.configuration import config
from pashword.core.sets import get

def digest(key: str, salt: str) -> bytes:
    """Return the hash value in binary."""
    algo = config.get(__name__, 'hash-algo')
    hashing = new(algo, usedforsecurity=True)
    hashing.update(key.encode('utf-8'))
    hashing.update(salt.encode('utf-8'))
    return hashing.digest()

def hexdigest(key: str, salt: str) -> str:
    """Return the hash value in hexadecimal."""
    return digest(key, salt).hex()

def password(key: str, salt: str, form: str) -> str:
    """Return the account password."""
    # get integer hash value
    bytes = digest(key, salt)
    index = int.from_bytes(bytes, byteorder='big', signed=False)
    # get resulting string
    word = []
    for metacharacter in form:
        characters = get(metacharacter)
        size = len(characters)
        word.append(characters[index%size])
        index //= size
    word = ''.join(word)
    return word

def save(key: str, path: str) -> None:
    """Save a hash of the key in a file."""
    salt = str(uuid4())
    data = {
        'salt': salt,
        'hash': hexdigest(key, salt),
    }
    with open(path, 'w') as file:
        dump(data, file)

def same(key: str, path: str) -> bool:
    """Return wether the key is the same as the one from the file."""
    with open(path, 'r') as file:
        data = load(file)
    return data['hash'] == hexdigest(key, data['salt'])
