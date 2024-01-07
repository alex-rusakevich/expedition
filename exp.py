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
        "-v", "--version", help="print version and exit", action="store_true"
    )

    subparsers = parser.add_subparsers()

    init_subp = subparsers.add_parser("init", help="initialize and empty artifact")
    init_subp.set_defaults(func=expedition.commands.init_command)

    del_subp = subparsers.add_parser("del", help="delete all the expedition files")
    del_subp.set_defaults(func=expedition.commands.del_command)
    del_subp.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="don't ask for permission before deleting",
    )

    build_subp = subparsers.add_parser("build", help="build an artifact .art file")
    build_subp.set_defaults(func=expedition.commands.build_command)
    build_subp.add_argument(
        "-o",
        "--output-dir",
        type=str,
        help="the directory for resulting .art file",
        default="build/",
    )

    install_subp = subparsers.add_parser("install", help="install an artifact")
    install_subp.set_defaults(func=expedition.commands.install_command)

    unitpath_subp = subparsers.add_parser(
        "unitpath", help="generate unitpath for all the modules installed"
    )
    unitpath_subp.set_defaults(func=expedition.commands.unitpath_command)

    args = parser.parse_args()

    if args.version:
        print(expedition.__version__)
        sys.exit()

    args.func(args)


if __name__ == "__main__":
    main()
