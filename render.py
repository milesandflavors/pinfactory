# -*- coding: utf-8 -*-
"""
Miles & Flavors — Pin Factory
Reads pins.csv (the v8 production plan), pulls photos from input_images/<slug>/,
renders each pin in the brand style (same look as the HTML Pin Maker),
and saves finished PNGs into done/.  Also writes done/_scheduler.csv for the uploader.

Usage:
  python render.py                 -> render every pin that has photos
  python render.py 2-days-in-athens  -> render only one article (for testing)
"""
import csv, os, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "input_images")
DONE = os.path.join(ROOT, "done")
FONTS = os.path.join(ROOT, "fonts")
PINS = os.path.join(ROOT, "pins.csv")
os.makedirs(DONE, exist_ok=True)

W, H = 1000, 1500
TERRA = (196, 132, 90)
WHITE = (255, 255, 255)
EXT = (".jpg", ".jpeg", ".png", ".webp")

def cluster(s):
    if 'athens' in s: return 'Athens'
    if 'rome' in s: return 'Rome'
    if 'nyc' in s or 'new-york' in s: return 'NYC'
    if 'greece' in s or 'zakynthos' in s or 'shipwreck' in s: return 'Greece'
    if 'amalfi' in s or 'southern-italy' in s: return 'Amalfi'
    if 'dolomite' in s or 'milan' in s: return 'Dolomites'
    if 'barcelona' in s: return 'Barcelona'
    if 'amsterdam' in s: return 'Amsterdam'
    if 'chicago' in s: return 'Chicago'
    if any(k in s for k in ['japan', 'tokyo', 'kyoto', 'osaka', 'hakone', 'ryokan']): return 'Japan'
    if 'marsa' in s: return 'Egypt'
    return 'Planning'

PLAYFAIR = os.path.join(FONTS, "PlayfairDisplay.ttf")
INTER = os.path.join(FONTS, "Inter.ttf")
_fc = {}
def font(path, size, weight):
    key = (path, size, weight)
    if key not in _fc:
        f = ImageFont.truetype(path, size)
        try: f.set_variation_by_axes([weight])
        except Exception: pass
        _fc[key] = f
    return _fc[key]

def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    nw, nh = int(im.width * s), int(im.height * s)
    im = im.resize((nw, nh), Image.LANCZOS)
    return im.crop(((nw - w) // 2, (nh - h) // 2, (nw - w) // 2 + w, (nh - h) // 2 + h))

def load(path):
    return Image.open(path).convert("RGB")

def imgs_in(d):
    if not d or not os.path.isdir(d): return []
    return sorted([f for f in glob.glob(os.path.join(d, "*")) if f.lower().endswith(EXT)])

def gradient_overlay(base, dark):
    # dark at top & bottom, light in the middle (legibility)
    def a(y):
        t = y / (H - 1)
        if t < .34:  v = dark + (dark*.12 - dark) * (t/.34)
        elif t < .66: v = dark*.12
        else: v = dark*.12 + (dark - dark*.12) * ((t-.66)/.34)
        return int(max(0, min(1, v)) * 255)
    col = Image.new("L", (1, H)); col.putdata([a(y) for y in range(H)])
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0)); grad.putalpha(col.resize((W, H)))
    return Image.alpha_composite(base, grad)

def bottom_scrim(base, strength=0.5, h=170):
    col = Image.new("L", (1, h)); col.putdata([int((i/(h-1))*strength*255) for i in range(h)])
    s = Image.new("RGBA", (W, h), (0, 0, 0, 0)); s.putalpha(col.resize((W, h)))
    base.alpha_composite(s, (0, H - h)); return base

def rrect_layer(box, fill_rgba, radius=10):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle(box, radius=radius, fill=fill_rgba)
    return ov

def _greedy(draw, words, fnt, limit):
    """Greedy wrap at a given width limit -> list of lines."""
    lines, ln = [], ""
    for w in words:
        t = (ln + " " + w).strip()
        if draw.textlength(t, font=fnt) > limit and ln:
            lines.append(ln); ln = w
        else:
            ln = t
    if ln: lines.append(ln)
    return lines

def wrap(draw, text, fnt, maxw):
    """Balanced word-wrap: uses the minimum number of lines, then evens the line
    widths so no short 'orphan' word is left dangling on its own line."""
    words = text.split()
    if not words: return []
    n = len(_greedy(draw, words, fnt, maxw))          # minimum lines that fit in maxw
    if n <= 1: return [text]
    # widest single word = hard lower bound for any line width
    minw = max(draw.textlength(w, font=fnt) for w in words)
    # binary-search the smallest width that still wraps into exactly n lines
    lo, hi, best = minw, maxw, maxw
    for _ in range(28):
        mid = (lo + hi) / 2.0
        if len(_greedy(draw, words, fnt, mid)) <= n:
            best = mid; hi = mid
        else:
            lo = mid
    return _greedy(draw, words, fnt, best)

def render_pin(template, bold, light, url, photos, dark=False, pale=False):
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    # ---- photos ----
    if template == "Split" and len(photos) >= 2:
        base.paste(cover(photos[0], W, H//2), (0, 0)); base.paste(cover(photos[1], W, H - H//2), (0, H//2))
    elif template == "Collage" and len(photos) >= 4:
        base.paste(cover(photos[0], W//2, H//2), (0, 0));     base.paste(cover(photos[1], W-W//2, H//2), (W//2, 0))
        base.paste(cover(photos[2], W//2, H-H//2), (0, H//2)); base.paste(cover(photos[3], W-W//2, H-H//2), (W//2, H//2))
    else:
        base.paste(cover(photos[0], W, H), (0, 0))

    busy = template in ("Split", "Collage")
    base = gradient_overlay(base, 0.30)
    if busy: base = bottom_scrim(base, 0.5, 170)

    d = ImageDraw.Draw(base)
    maxw = W - 160
    # auto-fit: shrink the font until the title fits compactly (bold <=2 lines, light <=2 lines),
    # so nothing overflows and the panel stays proportionate to the text.
    t1, t2 = 90, 80
    while True:
        fb = font(PLAYFAIR, t1, 700)
        fl = font(PLAYFAIR, t2, 400)
        L1 = wrap(d, bold, fb, maxw)
        L2 = wrap(d, light, fl, maxw) if light else []
        if (len(L1) <= 2 and len(L2) <= 2) or t1 <= 54:
            break
        t1 = int(t1 * 0.93); t2 = int(t2 * 0.93)
    lh1, lh2 = int(t1 * 1.12), int(t2 * 1.12)
    accent = template == "Accent" and light
    accentGap = 34 if accent else 0
    gapMid = 22 if light else 0
    blockH = len(L1) * lh1 + accentGap + gapMid + len(L2) * lh2

    if template in ("Title top", "Accent"): cy = int(H * 0.15)
    elif template == "Title bottom":        cy = int(H * 0.80) - blockH
    else:                                    cy = H // 2 - blockH // 2   # Centered/Split/Collage

    padX, padY = 52, 40
    # panel hugs the actual text: width = widest line + padding (not a full-width band)
    widest = max([d.textlength(l, font=fb) for l in L1] + ([d.textlength(l, font=fl) for l in L2] if L2 else [0]))
    panelW = min(W - 48, int(widest) + 2 * padX)
    bx0 = (W - panelW) // 2; bx1 = (W + panelW) // 2
    box = (bx0, max(0, cy - padY), bx1, min(H, cy + blockH + padY))
    # adaptive scrim: measure how bright the photo is behind the title; brighter -> stronger dark
    # scrim so the white text stays readable on light photos (cherry blossom, beaches, sky, etc.)
    mean = base.crop(box).convert("L").resize((1, 1)).getpixel((0, 0))  # average luminance 0-255
    a = max(0.0, min(0.58, (mean - 70) / 150))
    if busy: a = max(a, 0.46)
    if dark: a = max(0.58, min(0.82, (mean - 20) / 150))   # stronger scrim for hard-to-read photos
    elif pale: a = min(a, 0.26)                            # paler/lighter box
    base = Image.alpha_composite(base, rrect_layer(box, (0, 0, 0, int(a * 255))))
    base = Image.alpha_composite(base, rrect_layer(box, (242, 239, 234, 38)))   # subtle frosted tint on top
    d = ImageDraw.Draw(base)

    # ---- text onto a foreground layer (for a soft shadow) ----
    fg = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fg)
    y = cy
    for ln in L1:
        fd.text((W//2, y), ln, font=fb, fill=WHITE, anchor="ma"); y += lh1
    if accent:
        dw = int(min(130, maxw * 0.32))
        ImageDraw.Draw(base).rectangle((W//2 - dw//2, y + 16 - accentGap + 16, W//2 + dw//2, y + 16 - accentGap + 21), fill=TERRA)
        y += accentGap
    elif light:
        y += gapMid
    for ln in L2:
        fd.text((W//2, y), ln, font=fl, fill=WHITE, anchor="ma"); y += lh2
    # URL
    fd.text((W//2, H - 96), "  ".join(url), font=font(INTER, 30, 500), fill=WHITE, anchor="ma")

    # soft shadow from fg alpha
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(fg.split()[3].point(lambda a: int(a * 0.6)))
    sh = sh.filter(ImageFilter.GaussianBlur(5))
    base = Image.alpha_composite(base, sh)
    base = Image.alpha_composite(base, fg)
    return base.convert("RGB")

def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
    head = rows[0]; col = {name: i for i, name in enumerate(head)}
    made, skipped, missing = 0, 0, {}
    sched = []
    for r in rows[1:]:
        url = r[col["URL"]]; slug = url.replace("https://milesandflavors.com/", "").strip("/")
        if only and only != slug and only != cluster(slug): continue
        template = r[col["Template"]]; need = int(r[col["Photos"]])
        dark = template.endswith(" dark"); pale = template.endswith(" light")
        template = template.replace(" dark", "").replace(" light", "")
        bold = r[col["Pin bold (vastag)"]]; light = r[col["Pin light (vekony)"]]
        pin_no = r[col["Pin #"]]; datum = r[col["Datum"]]; idop = r[col["Idopont"]]
        board = r[col["Board"]]; pcim = r[col["Pin cim"]]; pdesc = r[col["Pin leiras"]]
        # photo lookup: 1) per-article override  2) city sub-folder (name appears in slug)  3) cluster root pool
        files = imgs_in(os.path.join(IMG_DIR, slug))
        if not files:
            cldir = os.path.join(IMG_DIR, cluster(slug))
            sub = None
            if os.path.isdir(cldir):
                for name in sorted(os.listdir(cldir)):
                    sd = os.path.join(cldir, name)
                    if os.path.isdir(sd) and name.lower() in slug and imgs_in(sd):
                        sub = sd; break
            files = imgs_in(sub) if sub else imgs_in(cldir)
        if len(files) == 0:
            skipped += 1; missing[slug] = need; continue
        # pick photos: rotate by pin number, cycle if fewer than needed
        start = (int(pin_no) - 1) % len(files)
        chosen = [files[(start + k) % len(files)] for k in range(need)]
        photos = [load(p) for p in chosen]
        img = render_pin(template, bold, light, "www.milesandflavors.com", photos, dark=dark, pale=pale)
        fname = f"{datum}_{idop.replace(':','-')}_{slug}_pin{pin_no}.png"
        img.save(os.path.join(DONE, fname), "PNG")
        sched.append([datum, idop, fname, board, pcim, pdesc, url])
        made += 1

    sched.sort(key=lambda x: (x[0], x[1]))
    with open(os.path.join(DONE, "_scheduler.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Datum", "Idopont", "Image file", "Board", "Pin cim", "Pin leiras", "URL"])
        w.writerows(sched)

    print(f"Rendered: {made} pins  ->  {DONE}")
    print(f"Skipped (no photos yet): {skipped}")
    if missing and not only:
        print(f"Article folders still needing photos: {len(missing)}")
        for s, n in sorted(missing.items())[:15]:
            print(f"   need {n}+ photo(s): input_images/{s}/")

if __name__ == "__main__":
    main()
