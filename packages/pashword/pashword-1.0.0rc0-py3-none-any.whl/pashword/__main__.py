# -*- coding: utf-8 -*-

"""Pashword command-line interface.

This module allows the user to launch the main features of the package
from a command-line interface.
"""

from argparse import ArgumentParser, BooleanOptionalAction

from pashword._version import version
from pashword.main import read, sort

features = (read, sort)

parser = ArgumentParser(
    prog=__package__,
    description=__doc__,
)

parser.add_argument('--version',
    action='version',
    version=f'%(prog)s {version}',
)

subparsers = parser.add_subparsers(
    dest='command',
    required=True,
    help="name of the feature to be used",
)

for module in features:
    name = module.__name__.split('.')[-1]
    help = module.main.__doc__
    subparser = subparsers.add_parser(name,
        help=help,
        description=module.__doc__,
    )
    for parameter, specification in module.PARAMETERS.items():
        args = [f'--{parameter}']
        kwargs = dict(specification)
        kwargs['metavar'] = kwargs.get('metavar', kwargs['type'].__name__)
        if 'default' in kwargs:
            kwargs['help'] += f" (default: {repr(kwargs['default'])})"
        else:
            kwargs['required'] = True
        if kwargs['type'] is bool:
            kwargs['action'] = BooleanOptionalAction
            kwargs['help'] = specification['help']
        subparser.add_argument(*args, **kwargs)

def main() -> None:
    """Parse arguments and call features."""
    args = parser.parse_args()
    for module in features:
        if args.command == module.__name__.split('.')[-1]:
            try:
                module.main(**vars(args))
            except Exception as exception:
                print(exception)
                exit(1)

if __name__ == '__main__':
    main()
