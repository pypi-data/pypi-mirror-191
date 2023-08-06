# -*- coding: utf-8 -*-

"""Init feature module.

This module implements the feature that allows to initialize a tree
tracker in a directory.
"""

from treecker.core.configuration import update
from treecker.core.snapshot import initialized, take, save

PARAMETERS = {
    'dir': {
        'help': "path to the tracked directory",
        'type': str,
        'default': '.',
    },
    'hash': {
        'help': "add the hash value to file signatures",
        'type': bool,
        'default': True,
    },
}

def main(**kwargs) -> None:
    """Create the first snapshot of a directory."""
    # retrieve parameters
    directory = str(kwargs['dir'])
    hash = bool(kwargs['hash'])
    # load configuration
    update(directory)
    # check that the directory is not already tracked
    if initialized(directory):
        raise Exception(f"treecker already initialized in {directory}")
    # initialize the tracker in the directory
    snap = take(directory, hash)
    save(directory, snap)
    print(f"treecker initialized in {directory}")
