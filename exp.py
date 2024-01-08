#!/usr/bin/env python3
import sys

assert sys.version_info >= (3, 8), "Python 3.8 or newer is required"

import argparse

import expedition
import expedition.commands
from expedition.settings import *


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

    update_subp = subparsers.add_parser(
        "update", help="retrieve info about packages from the repo"
    )
    update_subp.set_defaults(func=expedition.commands.update_command)
    update_subp.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="update the local package set info regardless of last modified time etc",
    )

    clear_subp = subparsers.add_parser("clear", help="delete expedition files")
    clear_subp.set_defaults(func=expedition.commands.clear_command)
    clear_subp.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="don't ask for permission before deleting",
    )
    clear_subp.add_argument(
        "mode",
        type=str,
        choices=["local", "cache"],
        help="clearing files mode",
        nargs="?",
        default="local",
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
    install_subp.add_argument(
        "artifacts",
        type=str,
        nargs="*",
        help="artifact names and versions or `file:///` paths",
    )
    install_subp.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["dev", "prod"],
        help="installation mode",
        default="dev",
    )

    unitpath_subp = subparsers.add_parser(
        "unitpath", help="generate unitpath for all the modules installed"
    )
    unitpath_subp.set_defaults(func=expedition.commands.unitpath_command)
    unitpath_subp.add_argument(
        "-m",
        "--mode",
        type=str,
        choices=["dev", "prod"],
        help="should unitpath include dev dependencies or not",
        default="dev",
    )

    args = parser.parse_args()

    if args.version:
        print(f"expedition v{expedition.__version__}")
        print_detected_compilers()
        sys.exit()

    if hasattr(args, "func"):
        args.func(args)
    else:
        print("Nothing to do, stopping...")


if __name__ == "__main__":
    main()
