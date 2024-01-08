import json
import os
import pathlib
import zipfile
from argparse import Namespace
from uu import encode

from expedition.settings import *
from expedition.util import *

dep_count = 0


def install_dependencies(dependencies: dict, mode: str = "dev"):
    global dep_count

    arts = dependencies["common"]

    if mode == "dev":
        arts = {**arts, **dependencies["dev"]}

    for name, path_or_ver in arts.items():
        print(f"Installing '{name}'='{path_or_ver}'...", end=" ")
        module_folder = ""

        if path_or_ver.startswith("file:///"):
            art_path = path_or_ver.replace("file:///", "", 1)
            module_folder = os.path.join(PASCAL_MODULES_DIR, name)
            pathlib.Path(module_folder).mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(
                art_path, "r", compression=zipfile.ZIP_DEFLATED, compresslevel=6
            ) as file:
                file.extractall(module_folder)

        dependencies = json.load(
            open(os.path.join(module_folder, "artifact.json"), "r", encoding="utf8")
        )["dependencies"]

        install_dependencies(dependencies, mode)

        dep_count += 1
        print("Done!")


def install_command(args: Namespace):
    global dep_count

    if not os.path.exists(MANIFEST_FILE_PATH):
        print("The expedition manifest file does not exist, stopping...")
        return

    if not args.artifacts:
        print(
            f"Installing dependencies from the manifest file ({args.mode.upper()} MODE)..."
        )
        manifest = json.load(open(MANIFEST_FILE_PATH, "r", encoding="utf-8"))

        install_dependencies(manifest["dependencies"], args.mode)

        print(f"All the {dep_count} dependencies where installed successfully")
