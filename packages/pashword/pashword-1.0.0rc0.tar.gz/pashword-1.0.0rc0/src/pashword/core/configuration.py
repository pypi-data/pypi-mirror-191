# -*- coding: utf-8 -*-

"""Configuration module.

This module provides a default configuration and a function for loading
a new configuration.
"""

from pkgutil import get_data
from configparser import ConfigParser
from os.path import join

config = ConfigParser()
config.read_string(get_data(__package__, 'default.conf').decode())

def update(directory: str) -> None:
    """Load the directory configuration."""
    file = config.get(__name__, 'file')
    path = join(directory, file)
    config.read(path)
