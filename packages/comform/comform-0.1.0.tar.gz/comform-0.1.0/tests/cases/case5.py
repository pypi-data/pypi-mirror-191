from comform.cli import FormatOptions
from comform.comments import Chunk, Comment

_NAME = "Block size increases."

_OPTIONS = FormatOptions(align=False, dividers=True, wrap=10)

_OLD_TEXT = """\
# 2345 78901
print("hello, world")
"""

_OLD_COMMENTS = [Comment(" 2345 78901", 1, 0, False)]

_NEW_TEXT = """\
# 2345
# 78901
print("hello, world")
"""

_OLD_CHUNKS = [Chunk(_OLD_COMMENTS)]

_NEW_CHUNKS = [Chunk([Comment(" 2345", 1, 0, False), Comment(" 78901", 2, 0, False)])]

DATA = _NAME, _OPTIONS, _OLD_TEXT, _OLD_COMMENTS, _OLD_CHUNKS, _NEW_CHUNKS, _NEW_TEXT
