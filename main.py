#!/usr/bin/env python3
"""Entry point: copy the pre-rendered poster to /output/entry.png.

Standard library only. The image is rendered by render_poster.py at
build time and shipped in this repository; this program only copies it
and verifies its SHA-256, so both runs write identical bytes.
"""
import hashlib
import os
import shutil
import sys

EXPECTED_SHA256 = "7bddd1c4257f8656b002d96c7756ee0864f242908050afc772a8bead36dd275f"


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    digest = hashlib.sha256(data).hexdigest()
    if digest != EXPECTED_SHA256:
        print(f"ERROR: entry.png sha256 mismatch: {digest}", file=sys.stderr)
        return 1
    with open(dst, "wb") as f:
        f.write(data)
    print(f"wrote {dst} ({len(data)} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
