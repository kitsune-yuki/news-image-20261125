#!/usr/bin/env python3
"""News-image entry: copy the finished front page beside this file
to the output directory.

The image itself (entry.png) was composed in this repository by
compose.py from the pixel-art illustration scene.png (drawn pixel by
pixel by pixel.py) and the 25 November 2026 news summary it carries.
This program does no network and no drawing, so both runs write
exactly the same bytes.

Run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DST_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(DST_DIR, exist_ok=True)
shutil.copyfile(SRC, os.path.join(DST_DIR, "entry.png"))
