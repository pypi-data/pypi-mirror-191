"""Test Short Cases.

For a number of small examples we test (nearly) every function of the `comform` program.
This allows for quick and easy identification of exactly which cases are failing, and/or
which functions have been broken.

Information for each test case `N` is in `tests.case.caseN`. Adding a new test case is
as simple as creating a new `tests.case.caseN` module in a similar format to the others.

Acts as unit tests for `fixes` and `comments` modules.
"""


from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from io import StringIO
from typing import Generator

import pytest

from comform.cli import FormatOptions
from comform.comments import Chunk, Comment, get_comments, to_chunks
from comform.fixes import _apply_fixes, _get_fixes, fix_text


@dataclass
class CaseData:
    # metadata
    num: int
    name: str
    # data
    options: FormatOptions
    old_text: str
    old_comments: list[Comment]
    old_chunks: list[Chunk]
    new_chunks: list[Chunk]
    new_text: str

    def __post_init__(self) -> None:
        self.old_lines = StringIO(self.old_text).readlines()
        self.new_lines = StringIO(self.new_text).readlines()
        self.fixes = list(zip(self.old_chunks, self.new_chunks))


def get_cases() -> Generator[CaseData, None, None]:
    n = 0
    while True:
        try:
            module = import_module(f"tests.cases.case{n}")
            yield CaseData(n, *module.DATA)
        except ModuleNotFoundError:
            return
        n += 1


CASES = list(get_cases())
pytestmark = pytest.mark.parametrize(
    argnames="data", argvalues=CASES, ids=[f"{case.num}. {case.name}" for case in CASES]
)


def test_get_comments(data: CaseData) -> None:
    actual_old_comments = list(get_comments(StringIO(data.old_text)))
    assert data.old_comments == actual_old_comments


def test_to_chunks(data: CaseData) -> None:
    actual_old_chunks = to_chunks(data.old_comments)
    assert data.old_chunks == actual_old_chunks


def test_get_fixes(data: CaseData) -> None:
    actual_fixes = _get_fixes(data.old_chunks, data.options)
    assert data.fixes == actual_fixes


def test_apply_fixes(data: CaseData) -> None:
    actual_new_lines = _apply_fixes(data.fixes, data.old_lines)
    assert data.new_lines == actual_new_lines


def test_fix_text(data: CaseData) -> None:
    # tests the above functions strung together; expect 1 failure above => this fails.
    actual_new_lines, actual_old_lines = fix_text(StringIO(data.old_text), data.options)
    assert actual_new_lines == data.new_lines
    assert actual_old_lines == data.old_lines
