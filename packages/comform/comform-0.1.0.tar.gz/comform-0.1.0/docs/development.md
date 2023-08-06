# Development details

My current development process for this repo. All subsequent sections assume the
following steps have been fulfilled:

1. Clone the repo with `git clone https://github.com/j-hil/comform.git`.
2. Navigate to the repo's root directory.
3. Create a virtual environment with `python -v venv .venv`.
4. Edit-ably install `comform` with dev requirements using `pip install -e .[dev]`.

## Writing code.

Develop on a branch off `main` and then raise a PR when ready and tests pass (this must
be manually checked).

Code should be written in styles dictated by the various linters and auto-formatters
used. Configurations can be found in [pyproject.toml](../pyproject.toml). This can most
easily be done through enabling `pre-commit` hooks (run `pre-commit install`).

## Build & Release

There is no formal release process - I do a release when I need access to an updated
version of the code through PyPI. The process for a release is:

1. Make sure the version number is set correctly in the code; bump if necessary.
2. Pick the commit to be published - it must be on the `main` branch.
3. Tag the commit with the version number with `git tag -a version_no` including any
   relevant notes in the tag text.
4. Build the package with `python -m build` then test
5. Publish with `python -m twine upload dist/*`.

## Testing

Tests are minimal but worth running. Either run `pytest tests` or to view coverage stats
run `coverage run -m pytest tests; coverage html`.
