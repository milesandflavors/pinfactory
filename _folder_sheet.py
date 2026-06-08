# -*- coding: utf-8 -*-
"""Build a labeled contact sheet for a list of article folders; print folder:idx:filename."""
import sys, os, glob
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.abspath(__file__))
folders = sys.argv[1:]
EXT = ('.jpg', '.jpeg', '.png', '.webp')
try: fnt = ImageFont.truetype(os.path.join(ROOT, 'fonts/Inter.ttf'), 26)
except: fnt = ImageFont.load_default()
cw, ch, perrow = 230, 250, 6
rows_img = []
mapping = []
for slug in folders:
    d = os.path.join(ROOT, 'input_images', slug)
    files = sorted([f for f in glob.glob(os.path.join(d, '*')) if f.lower().endswith(EXT)])
    nrows = (len(files) + perrow - 1) // perrow if files else 1
    sec = Image.new('RGB', (perrow * cw, nrows * ch + 34), (25, 25, 25))
    dd = ImageDraw.Draw(sec)
    dd.text((6, 4), slug[:46], font=fnt, fill=(255, 200, 120))
    for i, fp in enumerate(files):
        mapping.append((slug, i, os.path.basename(fp)))
        im = Image.open(fp).convert('RGB'); im.thumbnail((cw - 14, ch - 40))
        x = (i % perrow) * cw; y = 34 + (i // perrow) * ch
        sec.paste(im, (x + 7, y + 30))
        dd.rectangle((x + 4, y + 2, x + 44, y + 30), fill=(196, 132, 90))
        dd.text((x + 10, y + 2), str(i), font=fnt, fill=(255, 255, 255))
    rows_img.append(sec)
W = max(im.width for im in rows_img)
H = sum(im.height for im in rows_img) + 8 * len(rows_img)
sheet = Image.new('RGB', (W, H), (10, 10, 10))
yy = 0
for im in rows_img:
    sheet.paste(im, (0, yy)); yy += im.height + 8
sheet.save(os.path.join(ROOT, '_folders_preview.png'))
print('Mapping (folder | idx | file):')
for slug, i, fn in mapping:
    print(f'  {slug[:30]:30} {i:>2}  {fn}')
