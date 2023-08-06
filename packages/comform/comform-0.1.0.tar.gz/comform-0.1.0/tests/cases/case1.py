from comform.cli import FormatOptions
from comform.comments import Chunk, Comment

# Should cover all the same tests as those in tests.legacy
_NAME = "Legacy Test Case"

_OPTIONS = FormatOptions(align=False, dividers=True, wrap=88)

_OLD_TEXT = """\
# Block comment line 1
# Block comment line 2

print("hello, world")  # inline comment 1
print("bye")  # inline comment 2

# Final comment
"""

_OLD_COMMENTS = [
    Comment(" Block comment line 1", 1, 0, False),
    Comment(" Block comment line 2", 2, 0, False),
    Comment(" inline comment 1", 4, 23, True),
    Comment(" inline comment 2", 5, 14, True),
    Comment(" Final comment", 7, 0, False),
]

_NEW_TEXT = """\
# Block comment line 1 Block comment line 2

print("hello, world")  # inline comment 1
print("bye")  # inline comment 2

# Final comment
"""

_OLD_CHUNKS = [
    Chunk([_OLD_COMMENTS[0], _OLD_COMMENTS[1]]),
    Chunk([_OLD_COMMENTS[2], _OLD_COMMENTS[3]]),
    Chunk([_OLD_COMMENTS[4]]),
]

_NEW_CHUNKS = [
    Chunk([Comment(" Block comment line 1 Block comment line 2", 1, 0, False)]),
    Chunk([_OLD_COMMENTS[2], _OLD_COMMENTS[3]]),
    Chunk([_OLD_COMMENTS[4]]),
]

DATA = (_NAME, _OPTIONS, _OLD_TEXT, _OLD_COMMENTS, _OLD_CHUNKS, _NEW_CHUNKS, _NEW_TEXT)
