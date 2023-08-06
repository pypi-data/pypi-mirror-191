"""Unit tests for `comform.cli`."""
from __future__ import annotations

from comform.cli import get_options


def test_get_options() -> None:
    check, options, path_names = get_options(
        "--check --align --dividers --wrap 101 file1 file2 file3".split()
    )

    assert check
    assert options.align
    assert options.dividers
    assert options.wrap == 101
    assert path_names == ["file1", "file2", "file3"]

    check, options, path_names = get_options("file1 file2".split())
    assert not check
    assert not options.align
    assert not options.dividers
    assert options.wrap == 88
    assert path_names == ["file1", "file2"]


if __name__ == "__main__":
    test_get_options()
