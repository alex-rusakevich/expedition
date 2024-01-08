import bisect
import json
import os
import pathlib
import zipfile
from argparse import Namespace
from typing import Literal

from alive_progress import alive_bar

from expedition.settings import *
from expedition.util import *
from expedition.validator import validate_manifest

dependencies_to_install = []


def prepare_dependency_list(dependencies: dict, mode: Literal["dev", "prod"] = "dev"):
    global dependencies_to_install

    arts = dependencies["common"].items()

    if mode == "dev":
        arts = (*arts, *dependencies["dev"].items())

    for name, path_or_ver in arts:
        manifest = {}

        if path_or_ver.startswith("file:///"):  # local
            art_path = path_or_ver.replace("file:///", "", 1)

            with zipfile.ZipFile(
                art_path, "r", compression=zipfile.ZIP_DEFLATED, compresslevel=6
            ) as file:
                manifest = json.loads(file.read("artifact.json").decode("utf8"))
        else:  # repo
            ...

        bisect.insort(dependencies_to_install, (name, path_or_ver))
        prepare_dependency_list(manifest["dependencies"], mode)


def prepare_dependencies():
    global dependencies_to_install
    print("Preparing artifact files...")

    with alive_bar(len(dependencies_to_install)) as bar:
        for i, (name, path_or_ver) in enumerate(dependencies_to_install):
            print(f"Preparing '{name}': '{path_or_ver}'...", end=" ")

            if path_or_ver.startswith("file:///"):  # local
                art_path = path_or_ver.replace("file:///", "", 1)
                dependencies_to_install[i] = (name, art_path)
            else:  # repo
                ...

            print("Done!")
            bar()
    ...


def install_dependencies():
    global dependencies_to_install

    with alive_bar(len(dependencies_to_install)) as bar:
        for name, path in dependencies_to_install:
            print(f"Installing '{name}': '{path}'...", end=" ")
            module_folder = os.path.join(PASCAL_MODULES_DIR, name)
            pathlib.Path(module_folder).mkdir(parents=True, exist_ok=True)

            with zipfile.ZipFile(
                path, "r", compression=zipfile.ZIP_DEFLATED, compresslevel=6
            ) as file:
                validate_manifest(json.loads(file.read("artifact.json").decode("utf8")))
                file.extractall(module_folder)

            print("Done!")

            bar()


def install_command(args: Namespace):
    global dependencies_to_install
    print_detected_compilers()

    if not os.path.exists(MANIFEST_FILE_PATH):
        print("The expedition manifest file does not exist, stopping...")
        return

    if not args.artifacts:
        print(
            f"Installing dependencies from the manifest file ({args.mode.upper()} MODE)..."
        )
        manifest = json.load(open(MANIFEST_FILE_PATH, "r", encoding="utf-8"))

        print("Preparing the dependency list...", end=" ")
        prepare_dependency_list(manifest["dependencies"], args.mode)
        print("Done!", len(dependencies_to_install), "found.")

        prepare_dependencies()
        install_dependencies()
