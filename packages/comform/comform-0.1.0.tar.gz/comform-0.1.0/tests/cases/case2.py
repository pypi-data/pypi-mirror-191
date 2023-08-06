from comform.cli import FormatOptions
from comform.comments import Chunk, Comment

_NAME = "Check inline comments align."

_OPTIONS = FormatOptions(align=True, dividers=False, wrap=88)

_OLD_TEXT = """\
print("hello, world")  # inline comment 1
print("bye")  # inline comment 2
"""

_OLD_COMMENTS = [
    Comment(" inline comment 1", 1, 23, True),
    Comment(" inline comment 2", 2, 14, True),
]

_NEW_TEXT = """\
print("hello, world")  # inline comment 1
print("bye")           # inline comment 2
"""

_OLD_CHUNKS = [Chunk(_OLD_COMMENTS)]

_NEW_CHUNKS = [
    Chunk(
        [
            Comment(" inline comment 1", 1, 23, True),
            Comment(" inline comment 2", 2, 23, True),
        ]
    )
]

DATA = _NAME, _OPTIONS, _OLD_TEXT, _OLD_COMMENTS, _OLD_CHUNKS, _NEW_CHUNKS, _NEW_TEXT
