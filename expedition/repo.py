import os

import requests
from alive_progress import alive_bar

from expedition.settings import *
from expedition.util import *


def is_file_short_name_suits(file_short_name: str) -> bool:
    return True


def retrieve_package(name: str, desired_ver: str) -> str:
    """Find and download to cache or get from it a remote package and return path to .art file

    :param name: package name
    :type name: str
    :param ver: package version string with comparison signs
    :type ver: str
    :return: path to local file
    :rtype: str
    """
    if not name in get_local_pkg_set_manifest()["packages"]:
        raise FileNotFoundError(f"Unknown package name: {name}")

    file_cache_path = ""
    file_url = ""

    for pkg_ver, file_short_names in sorted(
        get_local_pkg_set_manifest()["packages"][name].items(), reverse=True
    ):
        if is_version_suitable(pkg_ver, desired_ver):
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

                    print(f"{gen_stairs(0)} Suitable version is '{name}': '{pkg_ver}'")

        if file_url:
            break

    if not file_cache_path:
        raise FileNotFoundError(
            f"Unable to find an artifact for '{name}': '{desired_ver}'"
        )

    if not (os.path.exists(file_cache_path) and os.path.isfile(file_cache_path)):
        file_size = get_file_size(file_url)
        print(f"{gen_stairs(1)} Downloading '{file_url}'...")

        with alive_bar(int(file_size / CHUNK_SIZE)) as bar:
            for _ in download_by_parts(file_url, file_cache_path):
                bar()
    else:
        print(f"{gen_stairs(1)} The file was found in cache.")

    return file_cache_path
