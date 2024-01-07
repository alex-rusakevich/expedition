import glob
import json
import os
import pathlib
import time
import zipfile
from argparse import Namespace

from expedition.settings import *
from expedition.util import *


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
