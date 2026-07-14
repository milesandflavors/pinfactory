# -*- coding: utf-8 -*-
"""
Miles & Flavors — Hybrid Pin Style (M&F × She Wanders Abroad)
Kísérlet: Lili terrakotta brandja + SWA-s alul-sáv layout + nagyobb szöveg hierarchia.

Különbségek a render.py-hoz képest:
  - Teljes szélességű terrakotta sáv alul (nem szűk lekerekített panel)
  - Főszöveg JÓVAL nagyobb (120px vs 90px)
  - Mindig alul-sávos elrendezés (Title bottom stílus)
  - Kisebb hook szöveg felette (elegáns, light)
  - Erősebb gradient az alul harmadban

Használat:
  python render_hybrid.py zakynthos-boat-tour   -> egy cikk tesztelése
  python render_hybrid.py 2-days-in-athens
  python render_hybrid.py best-things-to-do-in-london
"""
import csv, os, sys, glob
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageStat, ImageEnhance

ROOT   = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(ROOT, "input_images")
DONE   = os.path.join(ROOT, "done")
FONTS  = os.path.join(ROOT, "fonts")
PINS   = os.path.join(ROOT, "pins.csv")
os.makedirs(DONE, exist_ok=True)

W, H = 1000, 1500

# Brand colors
TERRA     = (196, 132, 90)      # terrakotta #C4845A
TERRA_ALT = (172, 108, 68)      # sötétebb terrakotta a sávhoz
WHITE     = (255, 255, 255)
CREAM     = (249, 246, 241)     # #F9F6F1

EXT = (".jpg", ".jpeg", ".png", ".webp")

# --- Font helpers (ugyanaz mint render.py) ---
PLAYFAIR = os.path.join(FONTS, "PlayfairDisplay.ttf")
INTER    = os.path.join(FONTS, "Inter.ttf")
_fc = {}
def font(path, size, weight=400):
    key = (path, size, weight)
    if key not in _fc:
        f = ImageFont.truetype(path, size)
        try: f.set_variation_by_axes([weight])
        except Exception: pass
        _fc[key] = f
    return _fc[key]

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

def cover(im, w, h):
    s = max(w / im.width, h / im.height)
    nw, nh = int(im.width * s), int(im.height * s)
    im = im.resize((nw, nh), Image.LANCZOS)
    return im.crop(((nw-w)//2, (nh-h)//2, (nw-w)//2+w, (nh-h)//2+h))

def load(path):
    return Image.open(path).convert("RGB")

def imgs_in(d, prefer_suffix=None):
    if not d or not os.path.isdir(d): return []
    files = sorted([f for f in glob.glob(os.path.join(d,"*")) if f.lower().endswith(EXT)],
                   key=os.path.getmtime, reverse=True)  # legfrissebb először
    # Pin-specifikus kép: pl. -2.jpg pin2-höz — ez megelőz mindent
    if prefer_suffix:
        preferred = [f for f in files
                     if os.path.splitext(os.path.basename(f))[0].endswith(prefer_suffix)]
        if preferred:
            return preferred + [f for f in files if f not in preferred]
    # EZT.jpg fallback (ha nincs pin-specifikus)
    ezt = [f for f in files if os.path.basename(f).upper() == "EZT.JPG"]
    return ezt + [f for f in files if f not in ezt] if ezt else files

def _greedy(draw, words, fnt, limit):
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
    words = text.split()
    if not words: return []
    n = len(_greedy(draw, words, fnt, maxw))
    if n <= 1: return [text]
    minw = max(draw.textlength(w, font=fnt) for w in words)
    lo, hi, best = minw, maxw, maxw
    for _ in range(28):
        mid = (lo + hi) / 2.0
        if len(_greedy(draw, words, fnt, mid)) <= n:
            best = mid; hi = mid
        else:
            lo = mid
    return _greedy(draw, words, fnt, best)


def find_best_zone(photo_rgb):
    """
    Megvizsgálja a fotó 3 harmadát és megkeresi ahol a legtöbb 'szabad tér' van
    (legkisebb variancia = legegyenletesebb kép = szöveg nem harcolna a háttérrel).
    Visszaad: 'top', 'middle', vagy 'bottom'
    """
    gray = photo_rgb.convert("L")
    zones = {
        "top":    gray.crop((0,        0,    W, H//3)),
        "middle": gray.crop((0,    H//3,     W, 2*H//3)),
        "bottom": gray.crop((0,    2*H//3,   W, H)),
    }
    scores = {}
    for name, zone in zones.items():
        stat   = ImageStat.Stat(zone)
        stddev = stat.stddev[0]   # alacsony = egyenletes = jó szöveg zóna
        mean   = stat.mean[0]
        # nagyon sötét (<45) vagy nagyon világos (>215) zóna kevésbé ideális
        legibility = 0.5 if (mean < 45 or mean > 215) else 1.0
        scores[name] = (1.0 / (stddev + 1)) * legibility
    best = max(scores, key=scores.get)
    # ha a különbség kicsi a bottom és a nyertes között → maradunk alul (Pinterest konvenció)
    if best != "bottom" and scores["bottom"] >= scores[best] * 0.82:
        best = "bottom"
    return best


def zone_gradient(base, zone):
    """Directional gradient a szöveg zóna szerint."""
    grad = Image.new("RGBA", (W, H), (0,0,0,0))
    pix  = []
    for y in range(H):
        t = y / (H - 1)
        if zone == "top":
            if t < 0.12:   a = int(0.42 * 255)
            elif t < 0.44: a = int((0.42 - (t-0.12)/0.32 * 0.36) * 255)
            else:           a = int(0.06 * 255)
        elif zone == "middle":
            dist = abs(t - 0.50)
            a = int((0.06 + dist * 0.88) * 255)
        else:  # bottom
            if t < 0.38:   a = 0
            else:
                frac = (t - 0.38) / 0.62
                a = int((frac ** 1.3) * 0.65 * 255)
        pix.append(min(255, a))
    col = Image.new("L", (1, H)); col.putdata(pix)
    grad.putalpha(col.resize((W, H)))
    return Image.alpha_composite(base, grad)


def adaptive_text_color(photo_rgb, text_zone_top):
    """
    Mintavételezi a fotót a szöveg zónájában (text_zone_top-tól aljáig),
    és visszaad egy (főszín, subszín) tuple-t ami harmonizál a fotóval.
    - Sötét fotó alj → fehér / krém
    - Világos fotó alj → sötét (terrakotta vagy mély barna)
    - Közepes → krém
    """
    zone = photo_rgb.crop((0, text_zone_top, W, H))
    lum = zone.convert("L").resize((1, 1)).getpixel((0, 0))  # átlag luminance

    if lum < 110:
        # sötét fotó → tiszta fehér + krém subtitle
        return WHITE, (249, 246, 241)
    else:
        # világos/közepes fotó → krém főcím + halvány krém subtitle
        # (terrakotta szöveg sehol sem szép — csak az accent vonalnak való)
        return (249, 246, 241), (230, 220, 210)


def parse_template(template):
    """Template oszlopból kiolvasja a zóna override-ot és az overlay erősségét."""
    t = template.lower()
    if "top" in t:
        zone_override = "top"
    elif "bottom" in t:
        zone_override = "bottom"
    elif "center" in t or "centred" in t or "centered" in t:
        zone_override = "middle"
    else:
        zone_override = None  # auto-detect (pl. "Accent")
    if "dark" in t:
        overlay_alpha = 100
        brightness = 1.0
    elif "light" in t:
        overlay_alpha = 28
        brightness = 1.10
    elif "medium" in t:
        overlay_alpha = 50
        brightness = 1.0
    else:
        overlay_alpha = 62
        brightness = 1.0
    return zone_override, overlay_alpha, brightness


def render_hybrid_pin(bold, light, photos, zone_override=None, overlay_alpha=90, brightness=1.0):
    """
    Hybrid layout v3 — SWA stílus, M&F betűkkel + adaptív szín.
      - Teljes fotó, semmi doboz/sáv
      - Csak enyhe gradient az alján (olvashatósághoz, nem "sávnak")
      - Nagy Playfair bold főcím + kisebb light subtitle (SWA hierarchia)
      - Terrakotta accent vonal (M&F brand)
      - Szöveg színe a fotóhoz igazodik (nem mindig fehér)
    """
    # 1. Fotó háttér
    base = Image.new("RGBA", (W, H), (0,0,0,255))
    raw_photo = cover(photos[0], W, H)
    if brightness != 1.0:
        raw_photo = ImageEnhance.Brightness(raw_photo).enhance(brightness)
    base.paste(raw_photo, (0, 0))

    # 2. Szöveg zóna: ha van Template override, azt használjuk; különben auto-detect
    zone = zone_override if zone_override else find_best_zone(raw_photo)

    # 3. Betűméretek — nagyobb subtitle mint korábban
    dummy = ImageDraw.Draw(Image.new("RGBA", (W, H)))
    maxw = W - 100
    t1, t2 = 112, 62          # t2 volt 50 → most 62 (nagyobb subtitle)
    while True:
        fb = font(PLAYFAIR, t1, 700)
        fl = font(PLAYFAIR, t2, 400)
        L1 = wrap(dummy, bold, fb, maxw)
        L2 = wrap(dummy, light, fl, maxw) if light else []
        if (len(L1) <= 3 and len(L2) <= 2) or t1 <= 58:
            break
        t1 = int(t1 * 0.92); t2 = int(t2 * 0.92)

    lh1, lh2 = int(t1 * 1.10), int(t2 * 1.18)
    acc_h, acc_gap = 5, 22

    if light:
        block_h = len(L2)*lh2 + acc_gap + acc_h + acc_gap + len(L1)*lh1
    else:
        block_h = len(L1)*lh1

    # 4. Szöveg pozíció a zóna szerint
    if zone == "top":
        block_bottom = int(H * 0.40)
    elif zone == "middle":
        block_bottom = int(H * 0.67)
    else:
        block_bottom = int(H * 0.91)
    text_top = block_bottom - block_h

    # 5. Adaptív szövegszín (fotó alapján, gradient ELŐTT mintavételezve)
    col_bold, col_light = adaptive_text_color(raw_photo, text_top - 40)

    # 6. Zóna-irányú gradient
    base = zone_gradient(base, zone)

    # 5. Halvány "légpárna" a szöveg mögé — alig látható, csak az olvashatóságért
    #    Nem doboz, hanem sötét elliptikus enyhe folt a szöveg területén
    pad_box = 30
    box_top    = text_top - pad_box
    box_bottom = int(H * 0.93)
    box_left   = W // 2 - maxw // 2 - pad_box
    box_right  = W // 2 + maxw // 2 + pad_box
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(overlay).rounded_rectangle(
        (box_left, box_top, box_right, box_bottom),
        radius=18,
        fill=(0, 0, 0, overlay_alpha)   # overlay erősség: Template dark/light/default
    )
    # Blur a széleken hogy ne legyen kemény vonal
    overlay = overlay.filter(ImageFilter.GaussianBlur(12))
    base = Image.alpha_composite(base, overlay)

    # 6. Szöveg réteg
    fg = Image.new("RGBA", (W, H), (0,0,0,0))
    fd = ImageDraw.Draw(fg)
    y = text_top

    # Subtitle / hook (SWA: kis szöveg a főcím FELETT)
    if light:
        for ln in L2:
            # Árnyék a subtitle mögé — extra kontrasztért mobil nézeten
            fd.text((W//2 + 2, y + 2), ln, font=font(PLAYFAIR, t2, 500),
                    fill=(0, 0, 0, 160), anchor="ma")
            fd.text((W//2, y), ln, font=font(PLAYFAIR, t2, 500),
                    fill=(*WHITE, 255), anchor="ma")
            y += lh2
        # Terrakotta accent vonal
        y += acc_gap
        dw = min(110, int(maxw * 0.26))
        ImageDraw.Draw(base).rectangle(
            (W//2 - dw//2, y, W//2 + dw//2, y + acc_h),
            fill=(*TERRA, 255))
        y += acc_h + acc_gap

    # Főcím — nagy, domináns
    for ln in L1:
        fd.text((W//2, y), ln, font=font(PLAYFAIR, t1, 700),
                fill=(*col_bold, 255), anchor="ma")
        y += lh1

    # URL
    fd.text((W//2, H - 48), "www.milesandflavors.com",
            font=font(INTER, 24, 400), fill=(*col_light, 150), anchor="ma")

    # Puha árnyék (csak ha a szöveg világos, azaz sötét fotón)
    if col_bold == WHITE or col_bold == (249, 246, 241):
        sh = Image.new("RGBA", (W, H), (0,0,0,0))
        sh.putalpha(fg.split()[3].point(lambda a: int(a * 0.75)))
        sh = sh.filter(ImageFilter.GaussianBlur(5))
        base = Image.alpha_composite(base, sh)

    base = Image.alpha_composite(base, fg)
    return base.convert("RGB")


def render_one(r, col):
    url_val = r[col["URL"]]
    slug = url_val.replace("https://milesandflavors.com/","").split("#")[0].strip("/")
    bold  = r[col["Pin bold (vastag)"]]
    light = r[col["Pin light (vekony)"]]
    pin_no = r[col["Pin #"]]

    pin_suffix = f"-{pin_no}" if pin_no and str(pin_no).isdigit() and int(pin_no) > 0 else None
    files = imgs_in(os.path.join(IMG_DIR, slug), prefer_suffix=pin_suffix)
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
        print(f"  [SKIP] Nincs fotó: {slug}"); return None

    # Foto oszlop: szám = 1-alapú index; fájlnév = adott kép; üres = legfrissebb
    foto_val = r[col["Foto"]].strip() if "Foto" in col else ""
    if foto_val and foto_val.isdigit() and int(foto_val) > 0:
        start = min(int(foto_val) - 1, len(files) - 1)
    elif foto_val:
        img_dir = os.path.join(IMG_DIR, slug)
        named = os.path.join(img_dir, foto_val)
        if os.path.isfile(named):
            start = next((i for i, f in enumerate(files) if os.path.basename(f) == foto_val), 0)
        else:
            start = 0
    else:
        start = 0  # mindig a legfrissebb kép (imgs_in mtime szerint sortol)

    # Template oszlop: zóna + overlay override
    template = r[col["Template"]].strip() if "Template" in col else ""
    zone_override, overlay_alpha, brightness = parse_template(template)

    photos = [load(files[start])]
    effective_zone = zone_override if zone_override else "bottom"
    img = render_hybrid_pin(bold, light, photos, zone_override=effective_zone, overlay_alpha=overlay_alpha, brightness=brightness)
    datum = r[col["Datum"]].strip() if "Datum" in col else ""
    ido   = r[col["Idopont"]].strip().replace(":", "-") if "Idopont" in col else ""
    if datum and ido:
        fname = f"{datum}_{ido}_{slug}_pin{pin_no}.png"
    else:
        fname = f"{slug}_pin{pin_no}.png"
    img.save(os.path.join(DONE, fname), "PNG")
    print(f"  OK: {fname}")
    return fname


def main():
    import datetime
    arg = sys.argv[1] if len(sys.argv) > 1 else None

    # Ha az arg dátum formátumú (YYYY.MM.DD), csak azt a napot rendeli
    # Ha slug/cluster, csak azokat rendeli
    # Ha nincs arg, csak a mai napot rendeli
    today_str = datetime.date.today().strftime("%Y.%m.%d")
    date_filter = None
    slug_filter = None

    if arg:
        import re
        if re.match(r"^\d{4}\.\d{2}\.\d{2}$", arg):
            date_filter = arg
        else:
            slug_filter = arg
    else:
        date_filter = today_str
        print(f"  [INFO] Csak mai pinek: {date_filter}")

    rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
    head = rows[0]; col = {name: i for i, name in enumerate(head)}
    made = 0

    for r in rows[1:]:
        if not r or not r[col["URL"]].startswith("http"): continue
        url_val = r[col["URL"]]
        slug = url_val.replace("https://milesandflavors.com/","").split("#")[0].strip("/")

        if date_filter:
            row_date = r[col["Datum"]].strip() if "Datum" in col else ""
            if row_date != date_filter:
                continue
        elif slug_filter:
            if slug_filter not in slug and slug_filter != cluster(slug):
                continue

        result = render_one(r, col)
        if result: made += 1

    print(f"\nElkészült: {made} pin  ->  {DONE}")


if __name__ == "__main__":
    main()
