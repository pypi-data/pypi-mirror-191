# -*- coding: utf-8 -*-

"""Issues feature module.

This module implements the feature that allows to check the file and
directory names.
"""

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
