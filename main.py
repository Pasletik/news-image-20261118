#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261118 bounty.

Copies the finished entry.png (which sits beside this file in the
repository) to $MAKEFUN_OUTPUT_DIR/entry.png. Standard library only,
no network, fully deterministic: the output is always byte-identical
to entry.png.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(
        os.path.join(here, "entry.png"),
        os.path.join(out_dir, "entry.png"),
    )


if __name__ == "__main__":
    sys.exit(main())
