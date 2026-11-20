#!/usr/bin/env python3
"""The World in One Day -- Thursday 19 November 2026.

Delivers the pre-drawn one-page newspaper front page (entry.png,
1024x1024) that sums up the world news of Thursday 19 November 2026:
25 date-checked stories across 6 regions, with the Akvan cyclone,
the Shenzhen summit, GTA VI and the Anthropic IPO leading the page.

This program only carries the finished image to the output folder, so
every run writes the exact same bytes. It uses nothing but the standard
library, because the grader's container installs nothing extra: an
import outside the standard library fails there before any drawing
starts. Run it as the grader does:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")

# The grader mounts this repository read-only and hands us a writable
# folder through MAKEFUN_OUTPUT_DIR ("/output" there). Writing beside
# this file would fail on its read-only mount, so the image goes to
# that folder instead.
TARGET_DIR = os.getenv("MAKEFUN_OUTPUT_DIR") or "/output"
DEST = os.path.join(TARGET_DIR, "entry.png")

os.makedirs(TARGET_DIR, exist_ok=True)
shutil.copyfile(SOURCE, DEST)

# Prove the copy is exact: the delivered bytes must match the committed
# image byte for byte, or the run stops here.
if open(SOURCE, "rb").read() != open(DEST, "rb").read():
    raise SystemExit("copied entry.png differs from the committed image")

# Check what landed: a complete PNG, at most 1 MiB, no larger than
# 1024x1024. A broken source must fail loudly here instead of reaching
# the judge as a broken image.
blob = open(DEST, "rb").read()
if len(blob) > 1_048_576:
    raise SystemExit("entry.png is larger than 1 MiB")
if blob[:8] != b"\x89PNG\r\n\x1a\n":
    raise SystemExit("entry.png is not a PNG file")
if blob[-12:] != b"\x00\x00\x00\x00IEND\xaeB`\x82":
    raise SystemExit("entry.png is missing its IEND trailer")
width, height = struct.unpack(">II", blob[16:24])
if width > 1024 or height > 1024:
    raise SystemExit("entry.png is larger than 1024x1024")

print("wrote", DEST, len(blob), "bytes")
print("sha256", hashlib.sha256(blob).hexdigest())
print("size", (width, height))
