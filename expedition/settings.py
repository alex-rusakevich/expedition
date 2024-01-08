import json
import logging
import logging.config
import os
import re
import subprocess
import sys
from pathlib import Path

from dotenv import load_dotenv

from expedition.util import *

load_dotenv("./.env", verbose=True)

MANIFEST_FILE_PATH = os.path.join(".", "artifact.json")
PASCAL_MODULES_DIR = os.path.join(".", "pascal_modules")

REPO_URL = "https://raw.githubusercontent.com/alex-rusakevich/archaelogical/main/"
CHUNK_SIZE = 1

AVAILABLE_COMPILERS = {}

# region Detect freepascal
try:
    fpc_output = subprocess.check_output(["fpc", "-h"]).decode()
    fpc_version = re.search(r"(?<=version\s).*(?=\s\[)", fpc_output).group(0)
    fpc_machine = re.search(r"(?<=for\s).*(?=\n)", fpc_output).group(0).strip()

    AVAILABLE_COMPILERS["freepascal"] = (str_to_ver(fpc_version), fpc_machine)
except FileNotFoundError:
    ...
# endregion

assert (
    AVAILABLE_COMPILERS != {}
), "No Pascal compilers detected in your PATH, stopping..."


def print_detected_compilers():
    print(
        "Detected:",
        ", ".join(
            f"{k} v{ver_to_str(v[0])} ({v[1]})" for k, v in AVAILABLE_COMPILERS.items()
        ),
    )


BASE_DIR: Path = Path(
    os.environ.get("EXP_BASE_DIR", os.path.join(os.path.expanduser("~"), ".expedition"))
)
LOG_DIR: Path = Path(os.path.join(BASE_DIR, "logs"))
CACHE_DIR: Path = Path(os.path.join(BASE_DIR, "cache"))

# region Process local pkgset manifest
LOCAL_PKG_SET_MANIFEST = None


def get_local_pkg_set_manifest():
    global LOCAL_PKG_SET_MANIFEST

    if os.path.exists(CACHE_DIR / "manifest.json") and os.path.isfile(
        CACHE_DIR / "manifest.json"
    ):
        LOCAL_PKG_SET_MANIFEST = json.load(
            open(CACHE_DIR / "manifest.json", "r", encoding="utf8")
        )
    else:
        raise FileNotFoundError(
            "Unable to find local package set manifest (cache/manifest.json). Did you run `exp update`?"
        )

    return LOCAL_PKG_SET_MANIFEST


# endregion

DEBUG: bool = os.environ.get("EXP_DEBUG", False) in ["t", True, "true"]
LOG_LVL: str = "DEBUG" if DEBUG else "INFO"
RESOURCE_PATH = Path(getattr(sys, "_MEIPASS", os.path.abspath(".")))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
    },
    "handlers": {
        "default": {
            "level": LOG_LVL,
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "report.log",
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 2,
            "formatter": "standard",
            "encoding": "utf8",
        },
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {"handlers": ["default", "console"], "level": LOG_LVL, "propagate": False},
        "invoke": {"handlers": ["default", "console"], "level": "WARNING"},
    },
}

BASE_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)
logging.config.dictConfig(LOGGING)

logger = logging.getLogger(__name__)
