from __future__ import annotations

from comform.cli import FormatOptions
from comform.comments import Chunk, Comment

_NAME = "No comment case."

_OPTIONS = FormatOptions(align=False, dividers=False, wrap=88)

_OLD_TEXT = """\
print("hello, world")
"""

_OLD_COMMENTS: list[Comment] = []

_NEW_TEXT = _OLD_TEXT

_OLD_CHUNKS: list[Chunk] = []

_NEW_CHUNKS: list[Chunk] = []

DATA = _NAME, _OPTIONS, _OLD_TEXT, _OLD_COMMENTS, _OLD_CHUNKS, _NEW_CHUNKS, _NEW_TEXT
