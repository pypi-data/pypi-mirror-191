# -*- coding: utf-8 -*-

"""Treecker command-line interface.

This module allows the user to launch the main features of the package
from a command-line interface.
"""

from argparse import ArgumentParser, BooleanOptionalAction

from treecker.main import init, status, commit, issues

parser = ArgumentParser(prog=__package__, description=__doc__)

subparsers = parser.add_subparsers(
    dest='command',
    required=True,
    help="name of the feature to be used",
)

for module in (init, status, commit, issues):
    name = module.__name__.split('.')[-1]
    help = module.main.__doc__
    subparser = subparsers.add_parser(name, help=help)
    for parameter, specification in module.PARAMETERS.items():
        args = [f'--{parameter}']
        kwargs = dict(specification)
        if kwargs['type'] is bool:
            kwargs['action'] = BooleanOptionalAction
        if not 'default' in kwargs:
            kwargs['required'] = True
        subparser.add_argument(*args, **kwargs)

def main() -> None:
    """Parse arguments and call features."""
    args = parser.parse_args()
    for module in (init, status, commit, issues):
        if args.command == module.__name__.split('.')[-1]:
            try:
                module.main(**vars(args))
            except Exception as exception:
                print(exception)
                exit(1)

if __name__ == '__main__':
    main()
