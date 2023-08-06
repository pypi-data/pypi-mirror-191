# Known Issues

## Limitations of formatting blocks as markdown

- Escaping of `_`. Specifically this can break links which aren't enclosed by backticks.
- Commented out code needs to be wrapped in triple-backticks or it will be wrecked.
  Given that commented out code is generally regarded as bad practice I don't see this
  as an issue.

## Missing Edge Cases

Cases I haven't checked, or that I know fail/misbehave.

- long headers

- sequential block comments differently aligned, eg:

  ```python
  for x in y:
      pass
      # in loop comment
  # out loop comment
  ```
