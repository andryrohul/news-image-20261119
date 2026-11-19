#!/usr/bin/env python3
"""Sum up 19 November's world news in one image.

Writes the pre-built front page (entry.png, 1024x1024, 130 KB) to
/output/entry.png. Standard library only, no network, deterministic:
the same bytes are written on every run.
"""
import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
OUT.mkdir(parents=True, exist_ok=True)
SRC = HERE / "entry.png"
DST = OUT / "entry.png"
shutil.copyfile(SRC, DST)

# Validate what was written: a whole PNG, at most 1 MiB and 1024x1024.
# Stdlib only, deterministic; a bad source fails loudly instead of
# submitting a broken image.
data = DST.read_bytes()
assert len(data) <= 1_048_576, "entry.png exceeds 1 MiB"
assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
assert data[-12:] == b"\x00\x00\x00\x00IEND\xaeB`\x82", "PNG missing IEND"
w, h = struct.unpack(">II", data[16:24])
assert w <= 1024 and h <= 1024, "image exceeds 1024x1024"
