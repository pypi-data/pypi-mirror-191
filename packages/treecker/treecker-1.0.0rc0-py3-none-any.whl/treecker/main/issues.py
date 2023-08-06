# -*- coding: utf-8 -*-

"""Main subpackage."""

from treecker.core.configuration import update
from treecker.core.snapshot import take
from treecker.core.naming import issues, issues_log

PARAMETERS = {
    'dir': {
        'help': "path to the tracked directory",
        'type': str,
        'default': '.',
    },
}

def main(**kwargs) -> None:
    """Display incorrectly named files and directories."""
    # retrieve parameters
    directory = str(kwargs['dir'])
    # load configuration
    update(directory)
    # retrieve the tree structure
    snap = take(directory, False)
    tree = snap['tree']
    # display recommendations
    listing = issues(tree)
    log = issues_log(listing)
    print(log)
