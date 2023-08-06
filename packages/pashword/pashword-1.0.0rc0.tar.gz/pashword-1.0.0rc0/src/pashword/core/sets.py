# -*- coding: utf-8 -*-

"""Character sets module.

This module provides the character sets used for the construction of
passwords.
"""

from pashword.core.configuration import config

def get(metacharacter: str) -> str:
    """Return the set of characters associated to the metacharacter."""
    return config.get(__name__, metacharacter, fallback=metacharacter)

def combinations(form: str) -> int:
    """Return the number of possible combinations for the given format."""
    number = 1
    for metacharacter in form:
        number *= len(get(metacharacter))
    return number
