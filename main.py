#!/usr/bin/env python3
"""Entry for make.fun news-image-20261121: ship the rendered front page as /output/entry.png."""
import os
import sys

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    with open(src, "rb") as f:
        data = f.read()
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)

if __name__ == "__main__":
    sys.exit(main())
