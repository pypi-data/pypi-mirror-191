# -*- coding: utf-8 -*-

"""Command1 module.

This module implements the functionality that allows...
"""

from os.path import join

from stemplate.core.configuration import update, config
from stemplate.core.feature import get_beginning, get_size

PARAMETERS = {
    'dir': {
        'help': "path to the directory",
        'type': str,
        'default': '.',
    },
    'file': {
        'help': "name of the file",
        'type': str,
    },
}

def main(**kwargs) -> None:
    """Read a file."""
    # retrieve parameters
    directory = str(kwargs['dir'])
    file = str(kwargs['file'])
    # load configuration
    update(directory)
    # do stuff
    path = join(directory, file)
    content = get_beginning(path)
    size = get_size(path)
    color = config.get(__name__, 'color')
    color = eval(f"'{color}'")
    colored = f"{color}{content}\033[0m"
    print(f"{colored} ...\n({size} bytes)")
