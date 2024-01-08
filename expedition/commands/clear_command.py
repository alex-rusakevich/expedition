import os
import shutil
from argparse import Namespace

from expedition.settings import *
from expedition.util import *


def clear_command(args: Namespace):
    if not os.path.exists(MANIFEST_FILE_PATH):
        print("The expedition manifest file does not exist, stopping...")
        return

    is_sure = args.force or (
        ask_for(
            f"Warning: you are about to delete the expedition {args.mode} files! Are you sure?",
            "n",
            ["y", "n"],
        )
        == "y"
    )

    if not is_sure:
        print("Stopping...")
        return

    if args.mode == "local":
        os.remove(MANIFEST_FILE_PATH)

        if os.path.exists(PASCAL_MODULES_DIR):
            shutil.rmtree(PASCAL_MODULES_DIR)

        print("The local expedition files where removed successfully!")
    elif args.mode == "cache":
        if os.path.exists(CACHE_DIR):
            shutil.rmtree(CACHE_DIR)

        print("The cache expedition files where removed successfully!")
