import json
import os
import sys
from argparse import Namespace

from expedition.settings import *
from expedition.util import *


def unitpath_command(args: Namespace):
    if not os.path.exists(MANIFEST_FILE_PATH):
        print("The expedition manifest file does not exist, stopping...")
        return

    manifest = json.load(open(MANIFEST_FILE_PATH, "r", encoding="utf-8"))
    dep_folders = []

    for k, _ in manifest["dependencies"]["common"].items():
        dep_folders.append(os.path.join(PASCAL_MODULES_DIR, k))

    if args.mode == "dev":
        for k, _ in manifest["dependencies"]["dev"].items():
            dep_folders.append(os.path.join(PASCAL_MODULES_DIR, k))

    dep_folders = tuple(os.path.normpath(p) for p in dep_folders)

    print(";".join(dep_folders))
