from comform.cli import FormatOptions
from comform.comments import Chunk, Comment

_NAME = "Check multiline strings are kept."

_OPTIONS = FormatOptions(align=True, dividers=False, wrap=88)

_OLD_TEXT = '''\
x = """This is a multi
line string"""
# comment
'''

_OLD_COMMENTS = [Comment(" comment", 3, 0, False)]

_NEW_TEXT = _OLD_TEXT

_OLD_CHUNKS = [Chunk(_OLD_COMMENTS)]

_NEW_CHUNKS = _OLD_CHUNKS

DATA = _NAME, _OPTIONS, _OLD_TEXT, _OLD_COMMENTS, _OLD_CHUNKS, _NEW_CHUNKS, _NEW_TEXT
