"""Basic code quality checks."""

import subprocess
from pathlib import Path

from mypy.api import run as run_mypy


def test_typing() -> None:
    _, _, exit_status = run_mypy(".".split())
    assert not exit_status


def test_style() -> None:
    path = Path(".") / "src" / "comform"
    subprocess.run(f"pylint {path}", capture_output=True, check=True)


if __name__ == "__main__":
    test_typing()
    test_style()
