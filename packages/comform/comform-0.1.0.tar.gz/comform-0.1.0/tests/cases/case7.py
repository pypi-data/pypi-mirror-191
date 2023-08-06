from __future__ import annotations

from comform.cli import FormatOptions
from comform.comments import Chunk, Comment

_NAME = "Inline comments with `align=False`"

_OPTIONS = FormatOptions(align=False, dividers=False, wrap=88)

_OLD_TEXT = """\
print("hello, world")  # bad     spacing
print("bye.")  #     worse    spacing        here
"""

_OLD_COMMENTS = [
    Comment(" bad     spacing", 1, 23, True),
    Comment("     worse    spacing        here", 2, 15, True),
]

_NEW_TEXT = """\
print("hello, world")  # bad spacing
print("bye.")  # worse spacing here
"""

_OLD_CHUNKS: list[Chunk] = [Chunk(_OLD_COMMENTS)]

_NEW_CHUNKS: list[Chunk] = [
    Chunk(
        [
            Comment(" bad spacing", 1, 23, True),
            Comment(" worse spacing here", 2, 15, True),
        ]
    )
]

DATA = _NAME, _OPTIONS, _OLD_TEXT, _OLD_COMMENTS, _OLD_CHUNKS, _NEW_CHUNKS, _NEW_TEXT
