# -*- coding: utf-8 -*-

"""Feature module.

This module provides...
"""

from os import stat

from stemplate.core.configuration import config

def get_beginning(path: str) -> str:
    """Return the content at the beginning of the file."""
    with open(path, 'r') as file:
        content = file.read()
    length = config.getint(__name__, 'length')
    shortened = content[:length]
    return shortened

def get_size(path: str) -> int:
    """Return the size of the file."""
    size = stat(path).st_size
    return size
