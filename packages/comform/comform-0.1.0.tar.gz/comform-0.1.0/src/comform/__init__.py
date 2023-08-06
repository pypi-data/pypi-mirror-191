"""API and metadata."""

from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path
from typing import Iterable, TextIO

from comform.cli import FormatOptions, get_options
from comform.fixes import fix_text
from comform.utils import gitignore_matches
from comform.version import __version__

__all__ = ["format_comments", "run", "__version__"]


def format_comments(
    # NOTE: keep in line with `comform.cli.FormatOptions`
    text: str | TextIO,
    align: bool = False,
    dividers: bool = False,
    wrap: int = 88,
) -> list[str]:
    """Format python comments in a string or text stream.

    :param text: Text to be formatted
    :param align: Align inline comments if true.
    :param dividers: Expand/shrink 'divider' comments if true.
    :param wrap: Column at which to wrap comments.
    :return: Formatted text.
    """
    if isinstance(text, str):
        text = StringIO(text)
    options = FormatOptions(align, dividers, wrap)
    new_lines, _ = fix_text(text, options)
    return new_lines


def _get_target_paths(path_name: str) -> Iterable[Path]:
    path = Path(path_name)
    if path.is_dir():
        return path.glob("**/*.py")
    if path.suffix == ".py":
        return [path]
    return []


def run(args: list[str] | None = None) -> None:
    """Entry point for `comform`.

    :param args: Command line arguments, defaults to reading from `sys.argv[1:]` but can
        be passed manually - see `comform -h` for usage.
    """
    if args is None:
        args = sys.argv[1:]

    check, options, path_names = get_options(args)

    altered = []
    for path_name in path_names:
        for path in _get_target_paths(path_name):
            if gitignore_matches(path):
                continue

            with open(path, encoding="utf-8") as fp:
                new_lines, old_lines = fix_text(fp, options)

            if new_lines == old_lines:
                continue
            altered.append(str(path))

            if check:
                print(f"*** Changes to {path_name}:", "-" * 99, sep="\n")
                print(*new_lines, "\n")
                continue
            with open(path, "w", encoding="utf-8") as fp:
                fp.writelines(new_lines)

    header = "*** Altered Files:" if not check else "*** Failed files:"
    print(header, *(altered if altered else ["\b(None)"]), sep="\n")
