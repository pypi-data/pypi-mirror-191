"""Example script to demonstrate the effectiveness of `comform`.

Use in regression testing.
"""

# -- Intro --------------------------------------------------------------------------- #

# Python (programming language) - source:
# `https://en.wikipedia.org/wiki/Python_(programming_language)`.
#
# Python is a high-level, general-purpose programming language. Its design philosophy
# emphasizes code readability with the use of significant indentation.
#
# Python is dynamically typed and garbage-collected. It supports multiple programming
# paradigms, including structured (particularly procedural), object-oriented and
# functional programming. It is often described as a "batteries included" language due
# to it's comprehensive standard library.

# Built-in types:
truth = True                              # Use `True` or `False`
hello_world = bytearray(b"hello, world")  # Mutable sequence of bytes
hello_there = bytes(b"hello there!")      # Immutable sequence of bytes
north_west = 2 + 2j                       # Complex numbers
# etc

# Python supports gradual typing. Python's syntax allows specifying static types, but
# they are not checked in the default implementation CPython. An experimental optional
# static type-checker, mypy, supports compile-time type checking.

from cmath import isclose, sqrt


def quadratic_root(a: complex, b: complex, c: complex, lesser: bool = False) -> complex:
    d = b**2 - 4 * a * c
    if lesser:
        return -(b + sqrt(d)) / (2 * a)
    return -(b - sqrt(d)) / (2 * a)


# golden ratio
assert isclose(quadratic_root(1, -1, -1), (1 + sqrt(5)) / 2)

# conjugate roots
root1 = quadratic_root(1, 2, 3)
root2 = quadratic_root(1, 2, 3, lesser=True)
assert isclose(root1, root2.conjugate())

# complex coefficients
root1 = quadratic_root(6, 23 - 1j, 23 + 1j)
root2 = quadratic_root(6, 23 - 1j, 23 + 1j, lesser=True)
assert isclose(root1, -(3 + 1j) / 2)
assert isclose(root2, (2j - 7) / 3)

# -- Maths --------------------------------------------------------------------------- #

# Excerpt from `https://en.wikipedia.org/wiki/Quadratic_formula`:
#
# > In elementary algebra, the quadratic formula is a formula that provides the
# > solution(s) to a quadratic equations. There are other ways of solving a quadratic
# > equation instead of using the quadratic formula such as factoring (direct factoring,
# > grouping, AC method), completing the square, graphing and others.
