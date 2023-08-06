# -*- coding: utf-8 -*-

"""Comparison module.

This module implements the comparison between two trees.
"""

from pathlib import Path

from treecker.core.configuration import config

def differences(old: dict, new: dict, hash: bool, path: list = []) -> list:
    """Return a list of the differences between two tree objects."""
    listing = []
    if isinstance(old, dict) and isinstance(new, dict):
        for n in old:
            if n in new:
                listing += differences(old[n], new[n], hash, path+[n])
            else:
                listing.append({'type': 'removed', 'path': path+[n]})
        for n in new:
            if not n in old:
                listing.append({'type': 'added', 'path': path+[n]})
    elif isinstance(old, dict) or isinstance(new, dict):
        listing.append({'type': 'removed', 'path': path})
        listing.append({'type': 'added', 'path': path})
    elif (old[0] != new[0]) or hash and (old[1] != new[1]):
        listing.append({'type': 'edited', 'path': path})
    return listing

def differences_log(differences: list) -> str:
    """Return a printable log of the differences."""
    colors = {
        'added': config.get(__name__, 'color-added'),
        'removed': config.get(__name__, 'color-removed'),
        'edited': config.get(__name__, 'color-edited'),
    }
    symbols = {
        'added': config.get(__name__, 'symbol-added'),
        'removed': config.get(__name__, 'symbol-removed'),
        'edited': config.get(__name__, 'symbol-edited'),
    }
    lines = []
    for diff in differences:
        type = diff['type']
        path = Path(*diff['path'])
        color = eval(f"'{colors[type]}'")
        symbol = symbols[type]
        line = f"{color}{symbol} {path} \033[0m"
        lines.append(line)
    if len(differences) == 0:
        lines.append(f"no change found")
    log = "\n".join(lines)
    return log
