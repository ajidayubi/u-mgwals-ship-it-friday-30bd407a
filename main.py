#!/usr/bin/env python3
"""Ship It Friday: the one commit message an AI coding agent writes
right before it breaks production on a Friday.

The program holds a single fixed line, checks it against the bounty's
gate (UTF-8 text, 1 to 159 characters, exactly one line, not only white
space, no leading or trailing white space), writes it to entry.txt in
the output directory, and reads the file back to confirm it round-trips
byte for byte.

Usage:
    python3 main.py

The output directory comes from $MAKEFUN_OUTPUT_DIR when set, else
/output. The program reads no input, calls no network, uses no clock
and no randomness, so every run writes the same bytes.
"""

import os
import sys

# The commit message, exactly one line. An upbeat agent ships at 4:59 PM
# on a Friday, sure the tests are green because they passed on its own
# machine, and breezily treats prod as staging with extra users. The
# joke lands on the last clause: the confidence is the disaster.
LINE = (
    "feat: deploy to prod Friday 4:59 PM \u2014 tests green on my machine, "
    "prod is just staging with more users"
)

GATE_MIN = 1
GATE_MAX = 159


def gate_error(line):
    """Return a human-readable gate failure, or None when the line passes."""
    if not isinstance(line, str):
        return "entry is not text"
    if line != line.strip():
        return "entry has leading or trailing white space"
    if not line.strip():
        return "entry is only white space"
    if "\n" in line or "\r" in line:
        return "entry spans more than one line"
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        return "entry is not valid UTF-8"
    if not GATE_MIN <= len(line) <= GATE_MAX:
        return "entry is %d characters, gate allows %d to %d" % (
            len(line),
            GATE_MIN,
            GATE_MAX,
        )
    return None


def run():
    error = gate_error(LINE)
    if error is not None:
        print("invalid entry: %s" % error, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    payload = LINE.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(payload)
    with open(path, "rb") as handle:
        stored = handle.read()
    if stored != payload:
        print("entry.txt did not round-trip byte for byte", file=sys.stderr)
        return 1
    if stored.decode("utf-8") != LINE:
        print("entry.txt did not round-trip to the same text", file=sys.stderr)
        return 1
    print(LINE)
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
