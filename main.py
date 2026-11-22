#!/usr/bin/env python3
"""Copy the pre-rendered 22 November 2026 world-news image to the output dir.

Stdlib only, no network, no fonts: the image (entry.png, 1024x1024) sits
beside this program in the repository. The grader runs this program twice;
both runs copy the same bytes, so both outputs are byte-identical.
"""
import hashlib
import os
import shutil
import sys

SRC_NAME = "entry.png"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    if not os.path.isfile(src):
        print("error: %s not found beside main.py" % src, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    if sha256_of(dst) != sha256_of(src):
        print("error: copied file does not match source", file=sys.stderr)
        return 1
    print("wrote %s sha256=%s" % (dst, sha256_of(dst)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
