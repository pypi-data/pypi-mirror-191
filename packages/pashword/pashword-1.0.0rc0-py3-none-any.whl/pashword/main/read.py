# -*- coding: utf-8 -*-

"""Read feature module.

This module implements the functionality that allows to search and
decode a password.
"""

from pathlib import Path
from getpass import getpass
from os.path import isfile

from pashword.core.configuration import update, config
from pashword.core.book import load, decode, filter
from pashword.core.hash import save, same
from pashword.core.sets import combinations

PARAMETERS = {
    'book': {
        'help': "path to the password book file",
        'type': str,
    },
    'hash': {
        'help': "path to the hash of the key",
        'type': str,
        'default': None,
    },
    'hide': {
        'help': "to hide passwords",
        'type': bool,
        'default': False,
    },
}

def main(**kwargs) -> None:
    """Find and display passwords."""
    # retrieve parameters
    book = str(kwargs['book'])
    hash = kwargs['hash']
    hide = bool(kwargs['hide'])
    # load configuration
    directory = Path(book).parent
    update(directory)
    color = {}
    for name, value in config[__name__].items():
        if name.startswith('color-'):
            color[name.replace('color-', '')] = eval(f"'{value}'")
    # load the password book
    data = load(book)
    file = f"{color['warn']}{Path(book).name}{color['stop']}"
    print(f"reading {file} ({len(book)} sections)")
    # filter accounts
    pattern = input(f"matching pattern: ")
    if pattern == '':
        print("exited")
        return
    filtered = filter(data, pattern)
    print(f"{len(filtered)} matching section(s) found")
    if len(filtered) == 0:
        return
    for name in filtered:
        print(f"- {color['name']}{name}{color['stop']}")
    # mode
    if hide:
        color_pash = color['hide']
        input_function = getpass
    else:
        color_pash = color['show']
        input_function = input
    # retrieve key
    stop = False
    while not stop:
        key = input_function("secret key: ")
        if key == '':
            print("exited")
            return
        if hash:
            if isfile(hash):
                stop = same(key, hash)
            else:
                stop = True
                save(key, hash)
                print(f"key hash saved in {hash}")
        else:
            stop = True
        if not stop:
            print(f"{color['warn']}incorrect secret key{color['stop']}")
    # decode
    decoded = decode(filtered, key)
    for name, entries in decoded.items():
        print(f"\n[{color['name']}{name}{color['stop']}]")
        for field, value in entries.items():
            if not field in ('password', 'form'):
                print(f"{field} = {value}")
        number = combinations(entries['form'])
        pash = f"{color_pash}{entries['password']}{color['stop']}"
        print(f"pash = {pash} ({number:1.0e})")
    input("\npress enter to exit")
