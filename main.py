#!/usr/bin/env python3
"""news-image-20261124 entrypoint (Python 3.13, standard library only).

Copies the finished front page, entry.png (1024x1024, drawn for this
entry by draw_image.py), to $MAKEFUN_OUTPUT_DIR/entry.png, after checking
it against the competition gate: PNG format with an IEND chunk, at most
1 MiB, at most 1024x1024 pixels. Fully offline and deterministic: two
runs write byte-identical output.
"""
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576
MAX_DIM = 1024


def read_png_size(path):
    """Return (width, height) from a PNG's IHDR chunk; raise on bad input."""
    with open(path, "rb") as f:
        head = f.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def check_png(path):
    size = os.path.getsize(path)
    if size > MAX_BYTES:
        raise ValueError("entry.png is %d bytes, over the 1 MiB cap" % size)
    width, height = read_png_size(path)
    if width > MAX_DIM or height > MAX_DIM:
        raise ValueError("entry.png is %dx%d, over the 1024x1024 cap"
                         % (width, height))
    with open(path, "rb") as f:
        tail = f.read()
    if not tail.rstrip(b"\x00").endswith(b"IEND" + struct.pack(">I", 0xAE426082)):
        raise ValueError("entry.png has no proper IEND chunk")
    return size, width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    size, width, height = check_png(src)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("wrote %s (%dx%d, %d bytes)" % (dst, width, height, size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
