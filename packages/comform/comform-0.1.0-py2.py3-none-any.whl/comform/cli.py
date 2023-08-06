"""Define the CLI."""

from __future__ import annotations

import sys
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from dataclasses import dataclass
from pathlib import Path

from comform.version import __version__

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib


@dataclass(frozen=True)
class FormatOptions:
    align: bool
    dividers: bool
    wrap: int


def get_options(args: list[str]) -> tuple[bool, FormatOptions, list[str]]:
    parser = ArgumentParser(
        prog="comform",
        description="Python Comment Conformity Formatter",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--version",
        "-v",
        action="version",
        help="print the version number",
        version=__version__,
    )
    parser.add_argument(
        "--check", "-c", action="store_true", help="do not write to files."
    )
    parser.add_argument(
        "--align", "-a", action="store_true", help="align in-line comments"
    )
    parser.add_argument(
        "--dividers", "-d", action="store_true", help="correct section divider comments"
    )
    parser.add_argument(
        "--wrap",
        "-w",
        default=None,
        type=int,
        help="Column at which to wrap comments",
        metavar="N",
    )
    parser.add_argument(
        "paths", nargs="+", help="folders/files to re-format (recursively)"
    )
    cmd_line_args = parser.parse_args(args)

    config_path = Path.cwd() / "pyproject.toml"
    if config_path.is_file():
        with open(config_path, "rb") as fp:
            config_args = tomllib.load(fp).get("tool", {}).get("comform", {})

    return (
        cmd_line_args.check or config_args.get("check", False),
        FormatOptions(
            cmd_line_args.align or config_args.get("align", False),
            cmd_line_args.dividers or config_args.get("dividers", False),
            cmd_line_args.wrap if cmd_line_args.wrap else config_args.get("wrap", 88),
        ),
        cmd_line_args.paths,
    )
