import re
from typing import Iterable, Optional, Sequence


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
    """Check if available version suits expected version condition. Uses Pascal-style signs

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
