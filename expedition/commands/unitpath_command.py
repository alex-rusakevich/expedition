import json
import os
from argparse import Namespace

from expedition.settings import *
from expedition.util import *

from .install_command import *


def unitpath_command(args: Namespace):
    if not os.path.exists(MANIFEST_FILE_PATH):
        print("The expedition manifest file does not exist, stopping...")
        return

    manifest = json.load(open(MANIFEST_FILE_PATH, "r", encoding="utf-8"))
    dep_folders = []

    prepare_dependency_list(manifest["dependencies"], mode=args.mode, silent=True)
    global dependencies_to_install

    for dep, _ in dependencies_to_install:
        dep_manifest = json.load(
            open(os.path.join(PASCAL_MODULES_DIR, dep, "artifact.json"))
        )
        dep_unitpath_root = dep_manifest["artifact"].get("unit_root", ".")
        dep_folders.append(os.path.join(PASCAL_MODULES_DIR, dep, dep_unitpath_root))

    dep_folders = set(os.path.normpath(p) for p in dep_folders)

    print(";".join(dep_folders))
