"""Orphan utility functions.

For functions which are sufficiently general to not really be part of the project
structure (namely they depend on no other code in `comform`):
- `zip_padded`; a generalization of `zip_longest`
- `format_as_md` & `format_line`; both wrappers around `mdformat.text`
-
"""

from __future__ import annotations

from itertools import zip_longest
from pathlib import Path
from typing import Any, Generator, Iterable, Literal, TypeVar, overload

import mdformat
from pathspec import PathSpec

_P = Path.cwd() / ".gitignore"
_GITIGNORE = PathSpec.from_lines("gitwildmatch", _P.open() if _P.is_file() else [])

_SENTINEL = object()

_T = TypeVar("_T")
_U = TypeVar("_U")
_V = TypeVar("_V")


@overload
def zip_padded(
    arg1: Iterable[_T],
    arg2: Iterable[_U],
    arg3: Iterable[_V],
    /,
    *,
    fillvals: tuple[_T, _U, _V],
) -> Generator[tuple[_T, _U, _V], None, None]:
    ...


@overload
def zip_padded(
    arg1: Iterable[_T], arg2: Iterable[_U], /, *, fillvals: tuple[_T, _U]
) -> Generator[tuple[_T, _U], None, None]:
    ...


def zip_padded(
    *args: Iterable[Any], fillvals: Iterable[Any]
) -> Generator[tuple[Any, ...], None, None]:
    for row in zip_longest(*args, fillvalue=_SENTINEL):
        yield tuple(v if v is not _SENTINEL else f for v, f in zip(row, fillvals))


def format_as_md(
    text: str,
    *,
    wrap: int | Literal["keep", "no"] = "keep",
    number: bool = False,
    eol: Literal["lf", "crlf", "keep"] = "lf",
) -> str:
    options = {"wrap": wrap, "number": number, "end-of-line": eol}
    return mdformat.text(text, options=options).strip()


def format_line(text: str) -> str:
    return format_as_md(text.strip(), wrap="no").strip()


def gitignore_matches(path: Path) -> bool:
    return _GITIGNORE.match_file(path.as_posix())
