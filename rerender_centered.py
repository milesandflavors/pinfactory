# -*- coding: utf-8 -*-
"""
Re-rendereli a jún. 19 22:00 – jún. 20 02:00 közötti 5 pint:
  - szövegdoboz középre (Centered)
  - picit sötétebb háttér (min scrim 0.35 az eredeti 0.0 helyett)
Felülírja a done/ mappában lévő fájlokat.
"""
import csv, os, sys, glob, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "input_images")
DONE    = os.path.join(ROOT, "done")
PINS    = os.path.join(ROOT, "pins.csv")
FONTS   = os.path.join(ROOT, "fonts")
OVR     = os.path.join(ROOT, "_photo_overrides.json")

W, H   = 1000, 1500
TERRA  = (196, 132, 90)
WHITE  = (255, 255, 255)
EXT    = (".jpg", ".jpeg", ".png", ".webp")

TARGET = {
    ("2026.06.19", "22:00"),
    ("2026.06.19", "23:00"),
    ("2026.06.20", "0:00"),
    ("2026.06.20", "1:00"),
    ("2026.06.20", "2:00"),
}

# ── helpers (másolt render.py-ból) ──────────────────────────────────────────
_fc = {}
def font(path, size, weight=400):
    key = (path, size, weight)
    if key not in _fc:
        f = ImageFont.truetype(path, size)
        try: f.set_variation_by_axes([weight])
        except Exception: pass
        _fc[key] = f
    return _fc[key]

PLAYFAIR = os.path.join(FONTS, "PlayfairDisplay.ttf")
INTER    = os.path.join(FONTS, "Inter.ttf")

def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    nw, nh = int(im.width * s), int(im.height * s)
    im = im.resize((nw, nh), Image.LANCZOS)
    return im.crop(((nw-w)//2, (nh-h)//2, (nw-w)//2+w, (nh-h)//2+h))

def load(path): return Image.open(path).convert("RGB")

def imgs_in(d):
    if not d or not os.path.isdir(d): return []
    return sorted([f for f in glob.glob(os.path.join(d,"*")) if f.lower().endswith(EXT)])

def gradient_overlay(base, dark_val):
    def a(y):
        t = y / (H - 1)
        if t < .34:  v = dark_val + (dark_val*.12 - dark_val) * (t/.34)
        elif t < .66: v = dark_val*.12
        else: v = dark_val*.12 + (dark_val - dark_val*.12) * ((t-.66)/.34)
        return int(max(0, min(1, v)) * 255)
    col = Image.new("L", (1, H)); col.putdata([a(y) for y in range(H)])
    grad = Image.new("RGBA", (W, H), (0,0,0,0)); grad.putalpha(col.resize((W, H)))
    return Image.alpha_composite(base, grad)

def rrect_layer(box, fill_rgba, radius=10):
    ov = Image.new("RGBA", (W, H), (0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle(box, radius=radius, fill=fill_rgba)
    return ov

def _greedy(draw, words, fnt, limit):
    lines, ln = [], ""
    for w in words:
        t = (ln + " " + w).strip()
        if draw.textlength(t, font=fnt) > limit and ln:
            lines.append(ln); ln = w
        else: ln = t
    if ln: lines.append(ln)
    return lines

def wrap(draw, text, fnt, maxw):
    words = text.split()
    if not words: return []
    n = len(_greedy(draw, words, fnt, maxw))
    if n <= 1: return [text]
    minw = max(draw.textlength(w, font=fnt) for w in words)
    lo, hi, best = minw, maxw, maxw
    for _ in range(28):
        mid = (lo + hi) / 2.0
        if len(_greedy(draw, words, fnt, mid)) <= n: best = mid; hi = mid
        else: lo = mid
    return _greedy(draw, words, fnt, best)

def render_centered_darker(bold, light, photos):
    """Centered template + min scrim 0.35 (picit sötétebb)."""
    base = Image.new("RGBA", (W, H), (0,0,0,255))
    base.paste(cover(photos[0], W, H), (0, 0))
    base = gradient_overlay(base, 0.30)

    d = ImageDraw.Draw(base)
    maxw = W - 160
    t1, t2 = 90, 80
    while True:
        fb = font(PLAYFAIR, t1, 700)
        fl = font(PLAYFAIR, t2, 400)
        L1 = wrap(d, bold, fb, maxw)
        L2 = wrap(d, light, fl, maxw) if light else []
        if (len(L1) <= 2 and len(L2) <= 2) or t1 <= 54: break
        t1 = int(t1 * 0.93); t2 = int(t2 * 0.93)
    lh1, lh2 = int(t1 * 1.12), int(t2 * 1.12)
    gapMid = 22 if light else 0
    blockH = len(L1) * lh1 + gapMid + len(L2) * lh2

    # ── KÖZÉPRE ──
    cy = H // 2 - blockH // 2

    padX, padY = 52, 40
    widest = max([d.textlength(l, font=fb) for l in L1] +
                 ([d.textlength(l, font=fl) for l in L2] if L2 else [0]))
    panelW = min(W - 48, int(widest) + 2 * padX)
    bx0 = (W - panelW) // 2; bx1 = (W + panelW) // 2
    box = (bx0, max(0, cy - padY), bx1, min(H, cy + blockH + padY))

    # ── PICIT SÖTÉTEBB: min 0.35 (eredeti 0.0) ──
    mean = base.crop(box).convert("L").resize((1,1)).getpixel((0,0))
    a = max(0.35, min(0.65, (mean - 50) / 130))

    base = Image.alpha_composite(base, rrect_layer(box, (0, 0, 0, int(a * 255))))
    base = Image.alpha_composite(base, rrect_layer(box, (242, 239, 234, 38)))
    d = ImageDraw.Draw(base)

    fg = Image.new("RGBA", (W, H), (0,0,0,0)); fd = ImageDraw.Draw(fg)
    y = cy
    for ln in L1:
        fd.text((W//2, y), ln, font=fb, fill=WHITE, anchor="ma"); y += lh1
    if light:
        y += gapMid
    for ln in L2:
        fd.text((W//2, y), ln, font=fl, fill=WHITE, anchor="ma"); y += lh2
    fd.text((W//2, H - 96), "  ".join("www.milesandflavors.com"),
            font=font(INTER, 30, 500), fill=WHITE, anchor="ma")

    sh = Image.new("RGBA", (W, H), (0,0,0,0))
    sh.putalpha(fg.split()[3].point(lambda a2: int(a2 * 0.6)))
    sh = sh.filter(ImageFilter.GaussianBlur(5))
    base = Image.alpha_composite(base, sh)
    base = Image.alpha_composite(base, fg)
    return base.convert("RGB")

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
    if any(k in s for k in ['japan','tokyo','kyoto','osaka','hakone','ryokan']): return 'Japan'
    if 'marsa' in s: return 'Egypt'
    return 'Planning'

# ── Fő logika ────────────────────────────────────────────────────────────────
overrides = json.load(open(OVR, encoding="utf-8")) if os.path.exists(OVR) else {}
rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]; col = {n: i for i, n in enumerate(head)}

for r in rows[1:]:
    datum = r[col["Datum"]]; idop = r[col["Idopont"]]
    if (datum, idop) not in TARGET: continue

    url    = r[col["URL"]]
    slug   = url.replace("https://milesandflavors.com/","").strip("/")
    bold   = r[col["Pin bold (vastag)"]]
    light  = r[col["Pin light (vekony)"]]
    pin_no = r[col["Pin #"]]

    # Fotó keresés
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

    if not files:
        print(f"SKIP (nincs fotó): {slug}"); continue

    start = (int(pin_no) - 1) % len(files)
    okey  = f"{slug}_pin{pin_no}"
    if okey in overrides:
        ov = os.path.join(IMG_DIR, slug, overrides[okey])
        chosen = ov if os.path.exists(ov) else files[start]
    else:
        chosen = files[start]

    photos = [load(chosen)]
    img = render_centered_darker(bold, light, photos)
    fname = f"{datum}_{idop.replace(':','-')}_{slug}_pin{pin_no}.png"
    out = os.path.join(DONE, fname)
    img.save(out, "PNG")
    print(f"OK: {fname}")

print("Kész.")
