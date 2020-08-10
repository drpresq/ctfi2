#!/bin/python3

import logging
import argparse

import gui


if __name__ == '__main__':
    log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    parser = argparse.ArgumentParser(description='ctfi2 - Remotely manage your CTFd server instance',
                                     epilog="GUI (-G) is default behavior")

    parser.add_argument('-G', action='store_true', help='Start the GUI')
    parser.add_argument('-C', action='store_true', help='Start the CLI')

    args = parser.parse_args()

    if args.C:
        pass

    elif args.G:
        gui.run(log_level)

    else:
        parser.print_help()
