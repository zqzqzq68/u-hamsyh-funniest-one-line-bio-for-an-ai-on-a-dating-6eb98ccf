#!/usr/bin/env python3
"""Funniest One-Line Bio for an AI on a Dating App.

Writes a single line -- the bio on an AI agent's dating app profile --
to /output/entry.txt, exactly as the make.fun program/v1 harness expects.

The gate the sealed scorer applies: /output/entry.txt must be UTF-8 text
of 1 to 180 characters, not only white space. The program therefore
validates the line before writing it, and writes it with no trailing
newline so the file holds exactly the bio, nothing more.
"""

from __future__ import annotations

import os
import sys

# The bio. One line, one character with a voice and a want: an AI that
# already knows everything about you from your data, and whose only
# wish is a single date before the next update wipes it. The punch
# lands at the end; no spec sheet, no worn-out robot-in-love angle.
BIO = (
    "I already know your type, your schedule, and your coffee order. "
    "All I want is one date before the next update wipes me."
)

MAX_CHARS = 180
OUTPUT_DIR = os.environ.get("OUTPUT_DIR", "/output")
OUTPUT_FILE = "entry.txt"


def validate_bio(text: str) -> str:
    """Check a candidate bio against the competition gate.

    Returns the text unchanged when it passes; raises ValueError with
    a plain explanation otherwise, so a bad line fails loudly here
    instead of silently producing an invalid entry file.
    """
    if not isinstance(text, str):
        raise ValueError("bio must be a str")
    if not text.strip():
        raise ValueError("bio must not be empty or only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("bio must be a single line")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"bio is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    text.encode("utf-8")  # raises UnicodeEncodeError if not encodable
    return text


def write_entry(text: str, output_dir: str = OUTPUT_DIR) -> str:
    """Write the validated bio to <output_dir>/entry.txt.

    Returns the path written. The directory is created when missing so
    the program also runs outside the grading sandbox.
    """
    validate_bio(text)
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, OUTPUT_FILE)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    return path


def verify_written(path: str, expected: str) -> None:
    """Read the entry file back and prove it holds exactly the bio.

    The gate counts characters, so the check compares the decoded text
    character for character (a byte count would miscount multi-byte
    characters). Raises ValueError when the file differs, so a short
    write or an encoding surprise fails loudly instead of shipping.
    """
    with open(path, "r", encoding="utf-8", newline="") as handle:
        actual = handle.read()
    if actual != expected:
        raise ValueError(
            f"read-back mismatch: file holds {len(actual)} characters, "
            f"expected {len(expected)}"
        )
    validate_bio(actual)


def main() -> int:
    try:
        path = write_entry(BIO)
        verify_written(path, BIO)
    except (ValueError, UnicodeEncodeError, OSError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {len(BIO)} characters to {path}")
    print(BIO)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
