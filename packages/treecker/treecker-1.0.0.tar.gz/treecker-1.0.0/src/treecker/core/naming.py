# -*- coding: utf-8 -*-

"""Naming module.

This module implements the naming check.
"""

from re import fullmatch
from pathlib import Path
from fnmatch import fnmatch

from treecker.core.configuration import config

def issues(tree: dict, path: list = []) -> list:
    """Return a list of the naming issues."""
    listing = []
    pattern = config.get(__name__, 'match')
    ignore = config.get(__name__, 'ignore').split()
    if isinstance(tree, dict):
        for name, child in tree.items():
            if fullmatch(pattern, name) is None:
                if not any([fnmatch(name, pattern) for pattern in ignore]):
                    text = f"{name} does not match {pattern}"
                    listing.append({'text': text, 'path': path+[name]})
            listing += issues(child, path+[name])
    return listing

def issues_log(issues: list) -> str:
    """Return a printable log of the naming issues."""
    lines = []
    color = config.get(__name__, 'color-issue')
    color = eval(f"'{color}'")
    for issue in issues:
        path = Path(*issue['path'])
        text = issue['text']
        line = f'{path} {color}{text}\033[0m'
        lines.append(line)
    if len(issues) == 0:
        lines.append("no issue found")
    log = "\n".join(lines)
    return log
