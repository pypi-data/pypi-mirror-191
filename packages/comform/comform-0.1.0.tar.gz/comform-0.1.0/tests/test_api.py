from __future__ import annotations

from io import StringIO
from typing import Any
from unittest.mock import Mock, mock_open, patch

from comform import format_comments, run
from comform.cli import FormatOptions

SCRIPT_PRE = """\
# Block comment line 1
# Block comment line 2

print("hello, world")  # inline comment 1
print("bye")  # inline comment 2

# Final comment
"""

SCRIPT_POST = """\
# Block comment line 1 Block comment line 2

print("hello, world")  # inline comment 1
print("bye")  # inline comment 2

# Final comment
"""
LINES_POST = StringIO(SCRIPT_POST).readlines()


def test_format() -> None:
    assert format_comments(SCRIPT_PRE) == LINES_POST


@patch("comform.open", new_callable=mock_open)
@patch("comform.print")
@patch("comform.get_options")
@patch("comform.fix_text")
def test_run(
    mock_fix_text: Mock,
    mock_get_options: Mock,
    mock_print: Mock,  # prevent writing to stdout during test
    mock_open: Mock,
) -> None:
    kwargs: dict[str, Any] = {"align": False, "dividers": False, "wrap": 88}
    mock_get_options.return_value = False, FormatOptions(**kwargs), ["file1.py"]

    fp1_mock = Mock()
    fp1_mock.__enter__ = Mock(return_value=fp1_mock)
    fp1_mock.__exit__ = Mock(return_value=False)
    mock_open.return_value = fp1_mock

    mock_fix_text.return_value = LINES_POST, []
    run()

    mock_get_options.return_value = True, FormatOptions(**kwargs), ["file1.py"]
    run()

    # Should only have been called on the first run:
    fp1_mock.writelines.assert_called_once_with(LINES_POST)


if __name__ == "__main__":
    test_format()
    test_run()
