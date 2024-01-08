from argparse import Namespace

from printree import ptree

from expedition.settings import *
from expedition.util import *

from .install_command import *


def list_command(args: Namespace):
    global dependencies_to_install

    if args.mode == "available":
        ptree(get_local_pkg_set_manifest()["packages"])
