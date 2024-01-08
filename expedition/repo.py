import os
from pathlib import Path

import requests

from expedition.settings import *
from expedition.util import *


def is_file_short_name_suits(file_short_name: str) -> bool:
    return True


def retrieve_package(name: str, ver: str) -> str:
    """Find and download to cache or get from it a remote package and return path to .art file

    :param name: package name
    :type name: str
    :param ver: package version string with comparison signs
    :type ver: str
    :return: path to local file
    :rtype: str
    """
    if not name in LOCAL_PKG_SET_MANIFEST["packages"]:
        raise FileNotFoundError(f"Unknown package name: {name}")

    file_cache_path = ""
    file_url = ""

    for pkg_ver, file_short_names in LOCAL_PKG_SET_MANIFEST["packages"][name].items():
        if is_version_suitable(pkg_ver, ver):
            for file_short_name in file_short_names:
                if is_file_short_name_suits(file_short_name):
                    file_url = joinurls(
                        REPO_URL,
                        name,
                        pkg_ver,
                        f"{name}-{pkg_ver}-{file_short_name}.art",
                    )
                    file_cache_path = os.path.join(
                        CACHE_DIR,
                        name,
                        pkg_ver,
                        f"{name}-{pkg_ver}-{file_short_name}.art",
                    )

        if file_url:
            break

    if not file_cache_path:
        raise FileNotFoundError(f"Unable to find an artifact for '{name}': '{ver}'")

    if os.path.exists(file_cache_path) and os.path.isfile(file_cache_path):
        return file_cache_path
    else:
        art_file = requests.get(file_url)
        print(file_url)

        if art_file.status_code == 200:
            Path(os.path.dirname(file_cache_path)).mkdir(parents=True, exist_ok=True)

            with open(file_cache_path, "wb") as file:
                file.write(art_file.content)

            return file_cache_path
        else:
            raise Exception(
                f"Unable to download artifact (code {art_file.status_code})"
            )
