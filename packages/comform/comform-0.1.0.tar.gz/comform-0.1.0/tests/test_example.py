"""Test a complex file example.

Serves as an integration test for all the code parts.
"""

import tempfile
from pathlib import Path

from comform import run

PATH_TO_PRE = Path(__file__).parent / "example_pre.py"
PATH_TO_POST = Path(__file__).parent / "example_post.py"


def test_comform_example() -> None:
    temp_file = Path(tempfile.NamedTemporaryFile(delete=False, suffix=".py").name)
    try:
        with open(PATH_TO_PRE) as pre_fp:
            old_text = pre_fp.read()

        with open(temp_file, "w") as temp_fp:
            temp_fp.write(old_text)

        run(["--align", "--dividers", str(temp_file)])

        with open(PATH_TO_POST) as post_fp:
            expected_new_text = post_fp.read()

        with open(temp_file) as temp_fp:
            actual_new_text = temp_fp.read()

        assert expected_new_text == actual_new_text
    finally:
        temp_file.unlink()


if __name__ == "__main__":
    test_comform_example()
