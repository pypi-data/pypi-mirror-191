# -*- coding: utf-8 -*-

"""Sort feature module.

This module implements the functionality that allows to sort a
password configuration file.
"""

from pathlib import Path

from pashword.core.configuration import update
from pashword.core.book import load, save

PARAMETERS = {
    'book': {
        'help': "path to the password book file",
        'type': str,
    },
}

def main(**kwargs) -> None:
    """Find and display passwords."""
    # retrieve parameters
    book = str(kwargs['book'])
    # load configuration
    directory = Path(book).parent
    update(directory)
    # load book
    data = load(book)
    # sort book
    ordered = {}
    for name in sorted(data.keys()):
        ordered[name] = data[name]
    # save book
    save(book, ordered)
