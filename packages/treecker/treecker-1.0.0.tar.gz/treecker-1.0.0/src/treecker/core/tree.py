# -*- coding: utf-8 -*-

"""Tree module.

This module implements the functionalities related to the trees.
"""

from hashlib import new
from os import stat
from pathlib import Path
from fnmatch import fnmatch
from multiprocessing import Pool

from treecker.core.configuration import config

def file_hash(path: Path) -> str:
    """Return the hash value of the file."""
    size = config.getint(__name__, 'block-size')
    algo = config.get(__name__, 'hash-algo')
    hashing = new(algo)
    with open(path, 'rb') as f:
        series = f.read(size)
        while len(series) > 0:
            hashing.update(series)
            series = f.read(size)
    hash = hashing.hexdigest()
    return hash

def file_size(path: Path) -> int:
    """Return the size of the file in bytes."""
    size = stat(path).st_size
    return size

def subtree_node(path: Path, ignore: list) -> dict:
    """Return the node representing the tracked element."""
    if path.is_file():
        node = [file_size(path)]
    elif path.is_dir():
        node = {}
        for entry in path.iterdir():
            relative = entry.relative_to(path)
            if not any([fnmatch(relative, pattern) for pattern in ignore]):
                node[entry.name] = subtree_node(entry, ignore)
    else:
        raise Exception(f"path '{path}' does not exist")
    return node

def tree_items(node: dict, path: list = []) -> list:
    """Flatten the tree."""
    items = []
    if isinstance(node, dict):
        for name, child in node.items():
            items += tree_items(child, path+[name])
    else:
        items.append((path, node))
    return items

def add_hash(directory: str, tree: dict) -> None:
    """Add the hash value to the file signatures."""
    items = tree_items(tree)
    items.sort(key=lambda item: item[1][0], reverse=True)
    paths = [Path(directory, *item[0]) for item in items]
    with Pool() as pool:
        hashs = pool.map(file_hash, paths, chunksize=1)
    for item, hash in zip(items, hashs):
        node = tree
        for entry in item[0]:
            node = node[entry]
        node.append(hash)

def tree_node(directory: str, ignore: list, hash: bool) -> dict:
    """Return the tree."""
    node = subtree_node(Path(directory), ignore)
    if hash:
        add_hash(directory, node)
    return node
