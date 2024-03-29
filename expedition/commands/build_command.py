import glob
import json
import os
import pathlib
import time
import zipfile
from argparse import Namespace

from expedition.settings import *
from expedition.util import *
from expedition.validator import validate_manifest


def build_command(args: Namespace):
    IGNORED_PATHS = [
        "pascal_modules/",
        "*.art",
        "build/",
        ".expignore",
        ".gitignore",
        ".git/",
        "node_modules/",
    ]

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
        path_to_check = os.path.normpath(path_to_check)
        path_to_check = os.path.abspath(
            os.path.expandvars(os.path.expanduser(path_to_check))
        )

        for p in IGNORED_PATHS:
            p = os.path.normpath(p)

            if path_to_check in [os.path.abspath(p) for p in glob.glob(p)]:
                # print(f"Skipping '{path_to_check}'...")
                return True

        return False

    if not os.path.exists(MANIFEST_FILE_PATH):
        print("The expedition manifest file does not exist, stopping...")
        return

    print("The building process has begun...")
    time_start = time.time()

    expedition_file = json.load(open(MANIFEST_FILE_PATH, "r", encoding="utf-8"))

    validate_manifest(expedition_file)

    output_file_path = (
        "{name}-{version}-{platform}-{machine}-{compiler}-{comp_ver}.art".format(
            name=expedition_file["artifact"]["name"],
            version=expedition_file["artifact"]["version"],
            platform=expedition_file["requirements"]["system"],
            machine=expedition_file["requirements"]["machine"],
            compiler=expedition_file["requirements"]["compiler"]["name"],
            comp_ver=comp_sign_to_latin(
                str(expedition_file["requirements"]["compiler"]["version"])
            ),
        )
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

        # print("DIR", dirname, "FILES", files)

        first_part = Path(dirname).parts[0] if dirname != "." else "."
        if is_path_ignored(dirname) or is_path_ignored(first_part):
            continue

        for filename in files:
            file_path = os.path.join(dirname, filename)

            if is_path_ignored(file_path):
                continue

            print(f"Adding '{file_path}' to the artifact...")
            zf.write(file_path)

    zf.close()
    # endregion

    time_spent = time.time() - time_start
    print(
        f"Done in {time_spent:.4f} seconds, the resulting artifact's path: '{os.path.abspath(output_file_path)}'"
    )
