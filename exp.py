#!/usr/bin/env python3
import sys

assert sys.version_info >= (3, 8), "Python 3.8 or newer is required"

import argparse

import expedition
import expedition.commands


def main():
    parser = argparse.ArgumentParser(
        description="Expedition: the Pascal package manager"
    )
    parser.add_argument(
        "--version", "-v", help="print version and exit", action="store_true"
    )

    subparsers = parser.add_subparsers()

    init_subp = subparsers.add_parser("init", help="initialize and empty artifact")
    init_subp.set_defaults(func=expedition.commands.init_command)

    del_subp = subparsers.add_parser("del", help="delete all the expedition files")
    del_subp.set_defaults(func=expedition.commands.del_command)

    args = parser.parse_args()

    if args.version:
        print(expedition.__version__)
        sys.exit()

    args.func()


if __name__ == "__main__":
    main()
