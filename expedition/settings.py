import re
import subprocess

MANIFEST_FILE_PATH = "./artifact.json"
PASCAL_MODULES_DIR = "./pascal_modules"

AVAILABLE_COMPILERS = {}

# region Detect freepascal
try:
    fpc_output = subprocess.check_output(["fpc", "-h"]).decode()
    AVAILABLE_COMPILERS["freepascal"] = re.search(
        r"(?<=version\s).*(?=\s\[)", fpc_output
    ).group(0)
except FileNotFoundError:
    ...
# endregion

assert AVAILABLE_COMPILERS != {}, "No Pascal compilers detected, stopping..."

print("Detected:", ", ".join(f"{k} v{v}" for k, v in AVAILABLE_COMPILERS.items()))
