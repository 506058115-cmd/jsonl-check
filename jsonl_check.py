#!/usr/bin/env python3
"""Validate JSON Lines records without echoing record contents."""

import argparse
import json
import sys
from pathlib import Path


def reject_non_json_constant(value):
    raise ValueError("non-standard numeric constant")


def inspect(path):
    valid = 0
    invalid = 0
    with path.open(encoding="utf-8-sig") as source:
        for line_number, line in enumerate(source, 1):
            if not line.strip():
                print(f"{path}:{line_number}: blank line is not a JSON record", file=sys.stderr)
                invalid += 1
                continue
            try:
                json.loads(line, parse_constant=reject_non_json_constant)
            except json.JSONDecodeError as error:
                print(
                    f"{path}:{line_number}:{error.colno}: invalid JSON ({error.msg})",
                    file=sys.stderr,
                )
                invalid += 1
            except ValueError as error:
                print(f"{path}:{line_number}: invalid JSON ({error})", file=sys.stderr)
                invalid += 1
            else:
                valid += 1
    return valid, invalid


def main():
    parser = argparse.ArgumentParser(
        description="Validate newline-delimited JSON without printing record values."
    )
    parser.add_argument("file", type=Path, help="UTF-8 JSON Lines file")
    args = parser.parse_args()
    try:
        valid, invalid = inspect(args.file)
    except (OSError, UnicodeError) as error:
        print(f"jsonl-check: {error}", file=sys.stderr)
        return 2
    print(f"{valid} valid record(s); {invalid} invalid line(s)")
    return 1 if invalid else 0


if __name__ == "__main__":
    raise SystemExit(main())
