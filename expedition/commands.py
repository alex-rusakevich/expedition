import glob
import json
import os
import pathlib
import shutil
import time
import zipfile
from argparse import Namespace

from expedition.util import *

AVAILABLE_COMPILERS = ("freepascal",)
EXPEDITION_FILE_PATH = "./expedition.json"
PASCAL_MODULES_DIR = "./pascal_modules"


def init_command(args: Namespace):
    basic_file = {
        "artifact": {"name": "example", "version": "0.0.1", "repo": ""},
        "requirements": {
            "platform": "any",
            "machine": "any",
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


def del_command(args: Namespace):
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


def build_command(args: Namespace):
    IGNORED_PATHS = ["pascal_modules/", "*.art", "build/"]

    # region Loading the file with paths to ignore
    if os.path.exists(".expignore") and os.path.isfile(".expignore"):
        print("Using the .expignore file...")

        with open(".expignore", "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()

                if line == "":
                    continue
                else:
                    IGNORED_PATHS.append(line)
    # endregion

    def is_path_ignored(path_to_check: str) -> bool:
        path_to_check = os.path.abspath(
            os.path.expandvars(os.path.expanduser(path_to_check))
        )

        for p in IGNORED_PATHS:
            if path_to_check in [os.path.abspath(p) for p in glob.glob(p)]:
                print(f"Skipping '{path_to_check}'...")
                return True

        return False

    if not os.path.exists(EXPEDITION_FILE_PATH):
        print("The expedition manifest file does not exist, stopping...")
        return

    print("The building process has begun...")
    time_start = time.time()

    expedition_file = json.load(open(EXPEDITION_FILE_PATH, "r", encoding="utf-8"))
    output_file_path = "{name}-{version}-{platform}-{machine}-{compiler}-{comp_min_ver}-{comp_max_ver}.art".format(
        name=expedition_file["artifact"]["name"],
        version=expedition_file["artifact"]["version"],
        platform=expedition_file["requirements"]["platform"],
        machine=expedition_file["requirements"]["machine"],
        compiler=expedition_file["requirements"]["compiler"]["name"],
        comp_min_ver=expedition_file["requirements"]["compiler"]["min_version"],
        comp_max_ver=expedition_file["requirements"]["compiler"]["max_version"],
    )

    pathlib.Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    output_file_path = os.path.join(args.output_dir, output_file_path)

    # region Making the artifact archive
    zf = zipfile.ZipFile(
        output_file_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6
    )

    for dirname, subdirs, files in os.walk("."):
        if dirname == "." and not files:
            continue

        if is_path_ignored(dirname):
            continue

        for filename in files:
            file_path = os.path.join(dirname, filename)

            if is_path_ignored(file_path):
                continue

            zf.write(file_path)

    zf.close()
    # endregion

    time_spent = time.time() - time_start
    print(
        f"Done in {time_spent:.4f} seconds, the resulting artifact's path: '{os.path.abspath(output_file_path)}'"
    )
