# -*- coding: utf-8 -*-

"""Book module.

This module implements functionalities to manipulate password books.
"""

from configparser import ConfigParser
from fnmatch import fnmatch

from pashword.core.configuration import config
from pashword.core.hash import password

def load(path: str) -> dict:
    """Return the data contained in the file."""
    config = ConfigParser()
    with open(path, 'r') as file:
        config.read_file(file)
    book = {}
    for name in config.sections():
        book[name] = dict(config[name])
    return book

def save(path: str, book: dict) -> None:
    """Save the book into a file."""
    config = ConfigParser()
    config.read_dict(book)
    with open(path, 'w') as file:
        config.write(file)

def filter(book: dict, pattern: str) -> dict:
    """Return the accounts whose name matches the pattern."""
    filtered = {}
    for name, account in book.items():
        if fnmatch(name, pattern):
            filtered[name] = account
    return filtered

def decode(book: dict, key: str) -> dict:
    """Return the book augmented with passwords."""
    decoded = {}
    for name, account in book.items():
        data = account.copy()
        form = data.pop('form')
        salt = ''.join(sorted(data.values())) + name
        word = password(key, salt, form)
        data = dict(**account, password=word)
        decoded[name] = data
    return decoded
