# -*- coding: utf-8 -*-

"""Snapshot module.

This module implements the functionalities related to the snapshots.
"""

from datetime import datetime, timezone
from pathlib import Path
from json import dumps as serialize, load as deserialize

from treecker.core.configuration import config
from treecker.core.tree import tree_node
from treecker._version import __version_tuple__

def take(directory: str, hash: bool) -> dict:
    """Return a snapshot of the directory."""
    file = config.get(__name__, 'file')
    ignore = config.get(__name__, 'ignore').split()
    ignore.append(file)
    date = datetime.now(timezone.utc).isoformat(timespec="seconds")
    node = tree_node(directory, ignore, hash)
    snapshot = {
        'version': __version_tuple__,
        'date': date,
        'hash': hash,
        'tree': node,
    }
    return snapshot

def save(directory: str, snapshot: dict) -> None:
    """Save the snapshot in the directory."""
    path = Path(directory) / config.get(__name__, 'file')
    with open(path, "w") as file:
        file.write(serialize(snapshot))

def load(directory: str) -> dict:
    """Load the last snapshot of the directory."""
    path = Path(directory) / config.get(__name__, 'file')
    with open(path, "r") as file:
        snapshot = deserialize(file)
    return snapshot

def initialized(directory: str) -> bool:
    """Check if the directory is tracked."""
    path = Path(directory) / config.get(__name__, 'file')
    return path.is_file()
