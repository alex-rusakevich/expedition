import os
import shutil
from argparse import Namespace

from expedition.settings import *
from expedition.util import *


def del_command(args: Namespace):
    if not os.path.exists(MANIFEST_FILE_PATH):
        print("The expedition manifest file does not exist, stopping...")
        return

    is_sure = (
        ask_for(
            "Warning: you are about to delete all the expedition files! Are you sure?",
            "no",
            ["yes", "no"],
        )
        == "yes"
    )

    if not is_sure:
        print("Stopping...")
        return

    os.remove(MANIFEST_FILE_PATH)
    shutil.rmtree(PASCAL_MODULES_DIR)

    print("The expedition files where removed successfully!")
