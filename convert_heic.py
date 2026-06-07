# -*- coding: utf-8 -*-
"""Convert every .HEIC photo under input_images/ to a .jpg next to it (originals kept).
The renderer can't read HEIC, so this makes iPhone photos usable."""
import os, glob
from PIL import Image
import pillow_heif
pillow_heif.register_heif_opener()

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(ROOT, "input_images")
n = 0
for path in glob.glob(os.path.join(IMG, "**", "*.HEIC"), recursive=True) + glob.glob(os.path.join(IMG, "**", "*.heic"), recursive=True):
    out = os.path.splitext(path)[0] + ".jpg"
    if os.path.exists(out):
        continue
    try:
        Image.open(path).convert("RGB").save(out, "JPEG", quality=92)
        n += 1
        print("  ->", os.path.relpath(out, IMG))
    except Exception as e:
        print("  FAILED", path, e)
print(f"Converted {n} HEIC file(s) to JPG")
