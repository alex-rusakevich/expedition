import json
import os
import pathlib
from argparse import Namespace

from expedition.settings import *
from expedition.util import *


def init_command(args: Namespace):
    basic_file = {
        "artifact": {
            "name": "example",
            "version": "0.0.1",
            "unit_root": ".",
            "description": "",
            "homepage": "",
            "author": "",
        },
        "requirements": {
            "platform": "any",
            "machine": "any",
            "compiler": {
                "name": "any",
                "version": "any",
            },
        },
        "dependencies": {"common": {}, "dev": {}},
    }

    assert not os.path.exists(
        MANIFEST_FILE_PATH
    ), "Cannot init an artifact: it was initialized already. \
Run `exp del` to remove all the expedition's files"

    basic_file["artifact"]["name"] = ask_for(
        "What is the name of your project?", "example"
    )
    basic_file["artifact"]["version"] = ask_for(
        "What is the version of your project?", "0.0.1"
    )

    basic_file["artifact"]["author"] = ask_for("Artifact's author", "")
    basic_file["artifact"]["description"] = ask_for("Artifact's description", "")
    basic_file["artifact"]["homepage"] = ask_for("Artifact's homepage", "")

    json.dump(basic_file, open(MANIFEST_FILE_PATH, "w", encoding="utf-8"), indent=2)
    pathlib.Path(PASCAL_MODULES_DIR).mkdir(exist_ok=True)

    print("Initialized the config successfully!")
