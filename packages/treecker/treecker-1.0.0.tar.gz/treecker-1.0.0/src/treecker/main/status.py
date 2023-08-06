# -*- coding: utf-8 -*-

"""Status feature module.

This module implements the feature that allows to display the changes
that have occurred in the tracked directory.
"""

from datetime import datetime, timezone

from treecker.core.configuration import update
from treecker.core.snapshot import initialized, load, take
from treecker.core.comparison import differences, differences_log

PARAMETERS = {
    'dir': {
        'help': "path to the tracked directory",
        'type': str,
        'default': '.',
    },
    'hash': {
        'help': "compare hash values",
        'type': bool,
    },
}

def main(**kwargs) -> None:
    """Display the changes since last snapshot."""
    # retrieve parameters
    directory = str(kwargs['dir'])
    hash = bool(kwargs['hash'])
    # load configuration
    update(directory)
    # check that the directory is tracked before loading latest snapshot
    if not initialized(directory):
        raise Exception(f"treecker not initialized in {directory}")
    snap1 = load(directory)
    # inform user
    date = datetime.fromisoformat(snap1['date'])
    zone = datetime.now(timezone.utc).astimezone().tzinfo
    date = date.astimezone(zone).isoformat(timespec="seconds")
    print(f"comparing with snapshot from {date} ({zone})")
    # hash or no hash
    hash1 = snap1['hash']
    if hash and not hash1:
        raise Exception("previous hash values not known")
    hash2 = hash
    if not hash2:
        print("comparison of files based on their size only")
    # display differences
    snap2 = take(directory, hash2)
    listing = differences(snap1['tree'], snap2['tree'], hash2)
    log = differences_log(listing)
    print(log)
