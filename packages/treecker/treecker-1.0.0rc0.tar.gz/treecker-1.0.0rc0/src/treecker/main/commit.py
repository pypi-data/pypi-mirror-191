# -*- coding: utf-8 -*-

"""Commit feature."""

from datetime import datetime, timezone

from treecker.core.configuration import update
from treecker.core.snapshot import initialized, load, take, save
from treecker.core.comparison import differences, differences_log

PARAMETERS = {
    'dir': {
        'help': "path to the tracked directory",
        'type': str,
        'default': '.',
    },
}

def main(**kwargs) -> None:
    """Save the changes in a new snapshot."""
    # retrieve parameters
    directory = str(kwargs['dir'])
    # load configuration
    update(directory)
    # check that the directory is tracked before loading latest snapshot
    if not initialized(directory):
        print(f"treecker not initialized in {directory}")
        exit(1)
    snap1 = load(directory)
    # inform user
    date = datetime.fromisoformat(snap1['date'])
    zone = datetime.now(timezone.utc).astimezone().tzinfo
    date = date.astimezone(zone).isoformat(timespec="seconds")
    print(f"comparing with snapshot from {date} ({zone})")
    # hash or no hash
    hash1 = snap1['hash']
    hash2 = hash1
    if not hash2:
        print("comparison of files based on their size only")
    # display differences
    snap2 = take(directory, hash2)
    listing = differences(snap1['tree'], snap2['tree'], hash2)
    log = differences_log(listing)
    print(log)
    # write new snapshot
    if len(listing) > 0:
        if not input(f"save modifications? (y/n) ").lower() == 'y':
            exit(0)
        save(directory, snap2)
        print(f"changes commited in {directory}")

