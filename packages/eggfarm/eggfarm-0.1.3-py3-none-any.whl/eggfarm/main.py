import sys
import os
from eggfarm.table_func_generator import generate_skeleton

import argparse
from distutils.util import strtobool

import importlib.metadata

package_metadada = importlib.metadata.metadata("eggfarm")
# info from pyproject.toml's `version` and `description`
EGGFARM_VERSION = package_metadada.get("Version")
EGGFARM_SUMMARY = package_metadada.get("Summary")


def _eggfarm_parser():
    parser = argparse.ArgumentParser(prog="eggfarm")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {EGGFARM_VERSION} [{EGGFARM_SUMMARY}]",
        help="show version number",
    )
    return parser


def _new_command_parser(sub_parsers):
    new_parser = sub_parsers.add_parser(
        "new",
        help="generate python table function skeleton",
    )

    new_parser.add_argument(
        "function_name",
        default=False,
        type=str,
        help="the name for the new table function, use `_` to connect multiple words (snake_case), e.g. `my_table_func`",
    )

    new_parser.add_argument(
        "-o",
        "--output-dir",
        type=str,
        required=False,
        help="specify the output directory for the new table function, default is `./<function_name>`",
    )


def parse_sys_args(sys_args):
    parser = _eggfarm_parser()
    sub_parsers = parser.add_subparsers(
        help=f"eggfarm generates python table function skeleton, version {EGGFARM_VERSION}",
        dest="command",
        required=True,
    )
    _new_command_parser(sub_parsers)
    args = parser.parse_args(sys_args)
    return vars(args)


def main():
    args = parse_sys_args(sys.argv[1:])
    sub_command = args["command"]

    actions = {
        "new": generate_skeleton,
    }
    actions[sub_command](args)
