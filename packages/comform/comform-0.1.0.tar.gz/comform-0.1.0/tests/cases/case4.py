from comform.cli import FormatOptions
from comform.comments import Chunk, Comment

_NAME = "Check indented blocks."

_OPTIONS = FormatOptions(align=False, dividers=True, wrap=20)

_OLD_TEXT = """\
if True:
    # 67890 2345 78901
    # line 2
    pass
"""

_OLD_COMMENTS = [
    Comment(" 67890 2345 78901", 2, 4, False),
    Comment(" line 2", 3, 4, False),
]

_NEW_TEXT = """\
if True:
    # 67890 2345
    # 78901 line 2
    pass
"""

_OLD_CHUNKS = [Chunk(_OLD_COMMENTS)]

_NEW_CHUNKS = [
    Chunk([Comment(" 67890 2345", 2, 4, False), Comment(" 78901 line 2", 3, 4, False)])
]

DATA = _NAME, _OPTIONS, _OLD_TEXT, _OLD_COMMENTS, _OLD_CHUNKS, _NEW_CHUNKS, _NEW_TEXT
