# jsonl-check

Validate newline-delimited JSON one record at a time. It reports line and column numbers but never echoes record contents, which is useful for large or sensitive exports.

## Use

Requires Python 3.8+; uses only the standard library.

```sh
python jsonl_check.py events.jsonl
```

Each nonblank line must contain one complete JSON value. Blank lines and non-standard numeric constants such as `NaN` are errors. The input is read only; an empty file is valid and contains zero records.

Exit status is `0` when all records are valid, `1` when one or more lines are invalid, and `2` when the file cannot be read.

## License

MIT
