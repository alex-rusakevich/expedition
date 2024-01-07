import json
import os
import pathlib
import shutil

from expedition.util import *

AVAILABLE_COMPILERS = ("freepascal",)
EXPEDITION_FILE_PATH = "./expedition.json"
PASCAL_MODULES_DIR = "./pascal_modules"


def init_command():
    basic_file = {
        "artifact": {"name": "example", "version": "0.0.1", "repo": ""},
        "requirements": {
            "platform": "any",
            "compiler": {
                "name": "freepascal",
                "min_version": None,
                "max_version": None,
            },
        },
        "dependencies": {"prod": [], "dev": []},
    }

    assert not os.path.exists(
        EXPEDITION_FILE_PATH
    ), "Cannot init an artifact: it was initialized already. \
Run `exp del` to remove all the expedition's files"

    proj_name = ask_for("What is the name of your project?", "example")
    proj_ver = ask_for("What is the version of your project?", "0.0.1")
    proj_compiler = ask_for(
        f"What is the compiler of your project?",
        "freepascal",
        AVAILABLE_COMPILERS,
    )
    proj_compiler_min_version = ask_for("Minimal compiler version", None)

    basic_file["artifact"]["name"] = proj_name
    basic_file["artifact"]["version"] = proj_ver

    basic_file["requirements"]["compiler"]["name"] = proj_compiler
    basic_file["requirements"]["compiler"]["min_version"] = proj_compiler_min_version

    json.dump(basic_file, open(EXPEDITION_FILE_PATH, "w", encoding="utf-8"), indent=4)
    pathlib.Path(PASCAL_MODULES_DIR).mkdir(exist_ok=True)

    print("Initialized the config successfully!")


def del_command():
    if not os.path.exists(EXPEDITION_FILE_PATH):
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

    os.remove(EXPEDITION_FILE_PATH)
    shutil.rmtree(PASCAL_MODULES_DIR)

    print("The expedition files where removed successfully!")
