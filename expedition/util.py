import posixpath
import re
from typing import Optional, Sequence
from urllib.parse import urljoin

import requests

import expedition.settings as es
from expedition.settings import *


def ask_for(label: str, default: Optional[str] = None, options: Sequence[str] = []):
    default_msg = f" (default is '{default}')" if default else ""
    cs_options = ""

    if type(options) != None:
        if len(options) >= 2:
            cs_options = (
                ", ".join([f"'{i}'" for i in options][:-1]) + f" and '{options[-1]}'"
            )
        else:
            cs_options = ", ".join([f"'{i}'" for i in options])

    options_msg = f" (options are {cs_options})" if options else ""
    input_msg = label + options_msg + default_msg + f": "
    input_msg = input_msg.replace(") (default", "; default")

    inp = input(input_msg).strip() or default

    if options and inp not in options:
        raise AssertionError(
            f"Unknown option: '{inp}', the available options are {cs_options}"
        )

    return inp


def is_version_suitable(available_version: str, expected_version: str) -> bool:
    """Check if available version suits expected version condition. Uses Pascal-style comparison signs

    Example:

    ```python
        is_version_suitable("0.0.1", "<>0.0.2") # => True
        is_version_suitable("0.0.3", ">0.0.2") # => True
        is_version_suitable("0.0.5", "<=0.0.2") # => False
    ```

    :param available_version: left part of condition
    :type available_version: str
    :param expected_version: right part of condition
    :type expected_version: str
    :return: result of comparing
    :rtype: bool
    """
    available_version = tuple(
        int(i) if i.isnumeric() else i for i in available_version.split(".")
    )

    expected_version = expected_version.strip()
    comparative_cmd = re.match(r"^<>|<=|>=|<|>|=", expected_version)

    version_right = None
    cmd_val = ""

    if comparative_cmd:
        cmd_val = comparative_cmd.group(0)
        expected_version = expected_version.replace(cmd_val, "", 1)

    version_right = tuple(
        int(i) if i.isnumeric() else i for i in expected_version.split(".")
    )
    available_version = tuple(available_version)

    if cmd_val in ["", "="]:
        return available_version == version_right
    elif cmd_val == "<>":
        return available_version != version_right
    elif cmd_val == "<":
        return available_version < version_right
    elif cmd_val == "<=":
        return available_version <= version_right
    elif cmd_val == ">":
        return available_version >= version_right
    elif cmd_val == ">=":
        return available_version >= version_right


def comp_sign_to_latin(version_cond: str, vice_versa=False) -> str:
    """Convert comparison signs on the beginning of version str to their latin equivalent (and back).
    Uses Pascal-style signs

    Example:

    ```python
        cond_to_latin("<0.0.2") # => "lt0.0.2"
        cond_to_latin("ne0.0.1", True) # => "<>0.0.1"
    ```

    :param version_cond: string with version condition, e.g. `>=0.0.1`
    :type version_cond: str
    :param vice_versa: should latin letters be converted back to condition marks?, defaults to False
    :type vice_versa: bool, optional
    :return: processed string
    :rtype: str
    """
    marks = {"<=": "lte", ">=": "gte", "<": "lt", ">": "gt", "<>": "ne", "=": ""}

    if vice_versa:
        version_cond = re.sub(r"^eq", "", version_cond, 1)

    for k, v in marks.items():
        if not vice_versa:
            if k in version_cond:
                version_cond = re.sub(r"^" + k, v, version_cond, 1)
                break
        else:
            if v in version_cond:
                if v != "":
                    version_cond = re.sub(r"^" + v, k, version_cond, 1)
                break

    return version_cond


def str_to_ver(string_in: str) -> tuple:
    """Convert a string with version to a tuple

    :param string_in: string with version, e.g. `"0.0.1.alpha"`
    :type string_in: str
    :return: tuple with version, e.g. `(0,0,1,"alpha")`
    :rtype: tuple
    """
    return tuple(int(num) if num.isnumeric() else num for num in string_in.split("."))


def ver_to_str(version: tuple) -> str:
    """Convert version tuple to a version string

    :param version: version tuple, e.g. `(0,0,1,"alpha")`
    :type version: tuple
    :return: resulting version string, e.g. `"0.0.1.alpha"`
    :rtype: str
    """
    return ".".join(tuple(str(num) for num in version))


def joinurls(*urls):
    return urljoin(urls[0], posixpath.join(*urls[1:]))


def download_by_parts(url: str, output_path: str) -> int:
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise Exception(f"Unable to download artifact (code {response.status_code})")

    with open(output_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=es.CHUNK_SIZE):
            f.write(chunk)
            yield es.CHUNK_SIZE


def get_file_size(url: str) -> int:
    head_resp = requests.request("HEAD", url, headers={"Accept-Encoding": "identity"})

    return int(head_resp.headers["content-length"])


def gen_stairs(lvl: int = 0):
    return (" " * 4 * lvl) + "└──"
