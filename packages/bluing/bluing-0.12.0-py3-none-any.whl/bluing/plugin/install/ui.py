#!/usr/bin/env python

r"""
Usage:
    bluing plugin install [-h | --help]
    bluing plugin install PATH

Arguments:
    PATH    The file path of a plugin package

Options:
    -h, --help    Print this help and quit
"""


import sys

from docopt import docopt
from xpycommon.log import Logger

from .. import BluingPluginManager
from . import LOG_LEVEL, PKG_NAME


logger = Logger(__name__, LOG_LEVEL)


def parse_cmdline(argv: list[str] = sys.argv[1:]) -> dict:
    logger.debug("Entered parse_cmdline(argv={})".format(argv))

    # In order to use `options_first=True` for strict compatibility with POSIX.
    # This replaces multi-level commands in `__doc__` with single-level commands.
    args = docopt(__doc__.replace(PKG_NAME.replace('.', ' '), PKG_NAME.split('.')[-1]), 
                  argv, help=False, options_first=True)
    logger.debug("docopt() returned\n"
                 "    args:", args)
    
    try:
        if args['--help'] or len(argv) == 0:
            print(__doc__)
            sys.exit()

        if args['PATH'] is not None and not BluingPluginManager.is_plugin(args['PATH']):
            raise ValueError("\"{}\" is not a valid plugin".format(args['PATH']))
    except Exception as e:
        logger.error("{}: \"{}\"".format(e.__class__.__name__, e))
        sys.exit(1)
    else:
        return args
