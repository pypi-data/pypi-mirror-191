# Plan

3 core parts: functionality, user interface, availability

## Part 1: Functionality

See below for proto-typical examples of the desired functionality and a rough idea of
how to implement it

### Aligned comments

Most formatters do the following:

```python
thing = my_func(
    arg1,  # this is a comment
    woah_another_arg,  # this arg is really important
    uncommented_arg,  #
    arg4,  # a blank comment needed to keep align
    wow_its_really_unclear_what_each_arg_does,  # people should implement kwargs :/
    arg6,  # last but not least
)
```

Meanwhile we want:

```python
# fmt: off
thing = my_func(
    arg1,                                       # this is a comment
    woah_another_arg,                           # this arg is really important
    uncommented_arg,                            #
    arg4,                                       # a blank comment needed to keep align
    wow_its_really_unclear_what_each_arg_does,  # people should implement kwargs :/
    arg6,                                       # last but not least
)
```

When a sequence of in-line comments encountered align based on which would be rightmost
after `black` formatting. Lots of edge cases to consider, like what about

```python
thing = (
    item1,  # in-line comment
    # this is an full line comment
    another_item,  # another comment
)
```

Should the comments be aligned? Maybe just the top and bottom two? I think this is rare
enough that I'll just make sure the behavior is sensible then leave it.

### Large Block Comments

```python
# This is a really complicated piece of code which requires lots of explanation
# but all the line lengths
# are different which is really annoying:
# * this bullet is ok
# * this bullet might have a lot of useful information but its
# very poorly formatted
# * oh dear
```

I think the best way to deal with this is just to rely on existing formatters - I think
that treating block comments as markdown text and using `mdformat` should work well and
facilitate incredibly flexible comments by giving a way to include ascii diagrams, code
snippets and more which won't be wrecked by `comform`.

With wrapping 50 (unusually short, but good for demo) this gives:

```python
# This is a really complicated piece of code which
# requires lots of explanation but all the line
# lengths are different which is really annoying:

# - this bullet is ok
# - this bullet might have a lot of useful
#   information but its very poorly formatted
# - oh dear
```

Issue found: `mdformat` replaces underscores in some places it shouldn't, eg in
`https://en.wikipedia.org/wiki/Cube_(algebra)`. This isn't a big issue since you can
just wrap the link in backticks but that's annoying to have to remember.

### Section Dividers

A single full line comment of the form `# -- title ----- #` should be automatically
expanded to fill the `--wrap` length.

This should be easy enough - match the comment using regex's and extend as appropriate.

### Comments to ignore

I should respect the comment directives of other formatters/linters etc, eg
`# type: ...`, `pylint: ...`, `noqa: ...` etc

I should also include `comforms` own 'ignore' comment direct add an ignore for comform,
maybe just piggy-back off `black`'s `fmt: off`.

Should I do anything special for commented out code - it would be expensive to check if
a code block is valid python code and its not like its good to encourage commenting out
code anyway. There are plenty of work arounds:

1. Using the `fmt: off` or equivalent
2. using in `if False: ...` block
3. adding a triple ticks around the comment

## Part 2: CLI & Config file

Create a standard command line interface using `argparse` in the style of many other
autoformatters (cf `black`, `mdformat` etc). Something like:

```
comform [-h] [--check] [--version] [--wrap INT] [--align]
```

where `--check` leaves the code unchanged, `--wrap` controls the desired max column
width of the file (default 88), and `--align` which will turn on aligning comments.

Each of the command line arguments should be alternately configurable in the usual
`pyproject.toml` file.

## Part 3: Pypi and Pre-commit integration

This should be available through `pypi` *and* as a `pre-commit` hook.

There will need to be 2 different versions of the `pre-commit` hooks, one that just runs
`comform` and another running `black` and `comform` in sequence.

This will alow `comform --align` to work with `black` - it will not otherwise since
`black` does not allow aligned comments.
