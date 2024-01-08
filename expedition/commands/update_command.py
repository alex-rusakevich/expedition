import os
from argparse import Namespace
from urllib.parse import urljoin

import requests

from expedition.settings import *


def update_local_pkg_manifest():
    manifest = requests.get(urljoin(REPO_URL, "manifest.json"))

    with open(CACHE_DIR / "manifest.json", "w", encoding="utf8") as f:
        f.write(manifest.text)

    with open(CACHE_DIR / "last_modified.txt", "w", encoding="utf8") as f:
        f.write(requests.get(urljoin(REPO_URL, "last_modified.txt")).text)

    # region Count statistics
    manifest_json = manifest.json()

    packages_num = len(manifest_json["packages"])
    versions_num = sum(len(pkg) for _, pkg in manifest_json["packages"].items())

    artifacts_num = 0
    for _, pkg in manifest_json["packages"].items():
        for _, ver in pkg.items():
            artifacts_num += len(ver)
    # endregion

    print(
        "The packages info was upgraded!",
        f"{packages_num} package(s), {versions_num} version(s) and {artifacts_num} artifact(s) are available now",
    )


def update_command(args: Namespace):
    if args.force:
        print("Force updating local package set info...")
        update_local_pkg_manifest()
        return

    if os.path.exists(CACHE_DIR / "manifest.json") and os.path.isfile(
        CACHE_DIR / "manifest.json"
    ):
        if os.path.exists(CACHE_DIR / "last_modified.txt") and os.path.isfile(
            CACHE_DIR / "last_modified.txt"
        ):
            local_last_mod = float(open(CACHE_DIR / "last_modified.txt").read())
            repo_last_mod = float(
                requests.get(urljoin(REPO_URL, "last_modified.txt")).text
            )

            if local_last_mod < repo_last_mod:
                print("Repo's package set info is newer than local, updating...")
            elif local_last_mod == repo_last_mod:
                print("Already up to date! Stopping...")
                return
            else:
                print("Local package info is newer than repo's? But how?.. Stopping...")
                return
        else:
            print(
                "Updating the package info due to absence of last_modified.txt file..."
            )

    update_local_pkg_manifest()
