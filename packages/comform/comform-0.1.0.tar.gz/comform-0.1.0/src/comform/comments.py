"""Retrieval and processing of comments."""

from __future__ import annotations

import tokenize
from dataclasses import dataclass
from token import COMMENT, INDENT, NEWLINE, NL
from typing import Generator, Iterable, List, TextIO, Tuple


@dataclass(frozen=True)
class Comment:
    __slots__ = "text", "lineno", "hash_col", "inline"

    text: str
    lineno: int
    hash_col: int
    inline: bool


class Chunk(List[Comment]):
    def __init__(self, _iterable: Iterable[Comment]) -> None:
        if not _iterable:
            raise ValueError("Do not allow an empty `Chunk`.")
        super().__init__(_iterable)

        repr_comment = self[0]
        self.start_lineno = repr_comment.lineno
        self.hash_col = repr_comment.hash_col
        self.inline = repr_comment.inline


Fixes = List[Tuple[Chunk, Chunk]]


def get_comments(fp: TextIO) -> Generator[Comment, None, None]:
    inline = False
    for token in tokenize.generate_tokens(fp.readline):
        if token.type in [NL, NEWLINE]:
            inline = False
        elif token.type is COMMENT:
            yield Comment(token.string[1:], *token.start, inline)
        elif token.type is not INDENT:
            inline = True


def to_chunks(comments: list[Comment]) -> list[Chunk]:
    if not comments:
        return []

    chunks = []
    prev_comment = comments[0]
    curr_chunk = Chunk([prev_comment])
    i = 1

    while i < len(comments):
        curr_comment = comments[i]

        if (
            curr_comment.lineno == prev_comment.lineno + 1
            and prev_comment.inline == curr_comment.inline
        ):
            curr_chunk.append(curr_comment)
        else:
            chunks.append(curr_chunk)
            curr_chunk = Chunk([curr_comment])

        prev_comment = curr_comment
        i += 1
    chunks.append(curr_chunk)

    return chunks
