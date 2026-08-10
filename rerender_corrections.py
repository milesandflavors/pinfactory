# -*- coding: utf-8 -*-
"""
Célzott pin-javítások: template pozíció, sötétség, fotócsere.
Felülírja a done/ mappában lévő fájlokat a meglévő nevükön.
"""
import csv, os, glob, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT  = os.path.dirname(os.path.abspath(__file__))
IMG   = os.path.join(ROOT, "input_images")
DONE  = os.path.join(ROOT, "done")
PINS  = os.path.join(ROOT, "pins.csv")
FONTS = os.path.join(ROOT, "fonts")
OVR   = os.path.join(ROOT, "_photo_overrides.json")
W, H  = 1000, 1500
WHITE = (255, 255, 255)
TERRA = (196, 132, 90)
EXT   = (".jpg", ".jpeg", ".png", ".webp")

# ── (slug, pin_no, new_template, dark, pale, photo_filename_override) ──────
# photo_filename_override: fájlnév az input_images/<slug>/ mappán belül, None = auto
CORRECTIONS = [
    # displaced (régi dátummal vannak done/-ban)
    ("day-trip-to-the-dolomites-from-venice", "2", "Centered", True,  False, None),
    ("hiking-in-the-dolomites",               "4", "Accent",   False, False, "ales-krivec-qH5wXNdTF_s-unsplash.jpg"),
    ("25-best-things-to-do-in-nyc",           "4", "Title bottom", False, False, None),
    ("best-things-to-do-in-marsa-alam-egypt-including-the-one-that-changes-everything",
                                              "4", "Accent",   False, False, "rafal-danhoffer-pjhlt7FZlkk-unsplash.jpg"),
    # jun.20
    ("5-day-new-york-city-itinerary",         "3", "Centered", True,  False, None),
    ("best-things-to-do-in-osaka",            "3", "Centered", True,  False, None),
    ("where-to-stay-in-marsa-alam",           "3", "Title bottom", True, False, None),
    # jun.21
    ("3-days-in-rome-itinerary",              "4", "Title bottom", False, False, None),
    ("where-to-stay-in-chicago-7-best-areas-hotels", "3", "Centered", False, False, None),
    ("free-stopover-flights-in-2026",         "1", "Centered", False, False, None),
    ("best-time-to-visit-the-azores",         "1", "Title bottom", False, False, None),
    ("12-day-greece-itinerary",               "4", "Accent",   False, True,  None),
    ("5-days-on-the-amalfi-coast-itinerary",  "4", "Title bottom", False, False, None),
    ("4-days-in-barcelona-the-perfect-itinerary", "4", "Title bottom", False, False, None),
    # jun.22
    ("japan-10-day-itinerary",                "4", "Title bottom", False, True,  None),
    ("best-travel-money-card",                "4", "Title bottom", False, False, None),
    ("free-things-to-do-in-marsa-alam",       "1", "Centered", False, False, None),
    ("2-days-in-athens",                      "4", "Title bottom", False, False, None),
    ("3-days-in-amsterdam",                   "4", "Centered", False, False, None),
    ("chicago-bucket-list-25-best-things-to-do", "4", "Centered", False, False, None),
    # jun.23
    ("barcelona-bucket-list",                 "4", "Centered", False, False, None),
    ("montserrat-day-trip-from-barcelona",    "1", "Centered", False, False, None),
    ("best-things-to-do-in-tokyo",            "4", "Title bottom", False, False, "sophie-keen-iYjerlfwBhA-unsplash.jpg"),
    ("amalfi-coast-bucketlist-25-best-thing-to-do", "4", "Title top", False, False, "1 amalfi positano.jpg"),
    # jun.24
    ("hakone-day-trip-from-tokyo",            "1", "Title top", False, True,  None),
    ("best-day-trips-from-amsterdam",         "4", "Centered", True,  False, None),
    ("best-beaches-in-zakynthos",             "4", "Accent",   False, True,  None),
    # jun.25
    ("zakynthos-road-trip-itinerary",         "1", "Title top", False, True,  None),
    ("where-to-stay-in-barcelona",            "4", "Centered", False, False, None),
    ("chicago-travel-costs-the-honest-budget-guide", "1", "Centered", False, False, None),
]

# ── helpers (render.py-ból másolva) ─────────────────────────────────────────
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
    s = max(w/im.width, h/im.height)
    nw, nh = int(im.width*s), int(im.height*s)
    im = im.resize((nw, nh), Image.LANCZOS)
    return im.crop(((nw-w)//2,(nh-h)//2,(nw-w)//2+w,(nh-h)//2+h))

def load(p): return Image.open(p).convert("RGB")

def imgs_in(d):
    if not d or not os.path.isdir(d): return []
    return sorted([f for f in glob.glob(os.path.join(d,"*")) if f.lower().endswith(EXT)])

def gradient_overlay(base, dark_val):
    def a(y):
        t = y/(H-1)
        if t<.34:  v = dark_val+(dark_val*.12-dark_val)*(t/.34)
        elif t<.66: v = dark_val*.12
        else: v = dark_val*.12+(dark_val-dark_val*.12)*((t-.66)/.34)
        return int(max(0,min(1,v))*255)
    col = Image.new("L",(1,H)); col.putdata([a(y) for y in range(H)])
    grad = Image.new("RGBA",(W,H),(0,0,0,0)); grad.putalpha(col.resize((W,H)))
    return Image.alpha_composite(base, grad)

def rrect_layer(box, fill_rgba, radius=10):
    ov = Image.new("RGBA",(W,H),(0,0,0,0))
    ImageDraw.Draw(ov).rounded_rectangle(box, radius=radius, fill=fill_rgba)
    return ov

def _greedy(draw, words, fnt, limit):
    lines, ln = [], ""
    for w in words:
        t = (ln+" "+w).strip()
        if draw.textlength(t,font=fnt)>limit and ln: lines.append(ln); ln=w
        else: ln=t
    if ln: lines.append(ln)
    return lines

def wrap(draw, text, fnt, maxw):
    words = text.split()
    if not words: return []
    n = len(_greedy(draw,words,fnt,maxw))
    if n<=1: return [text]
    minw = max(draw.textlength(w,font=fnt) for w in words)
    lo,hi,best = minw,maxw,maxw
    for _ in range(28):
        mid=(lo+hi)/2.0
        if len(_greedy(draw,words,fnt,mid))<=n: best=mid; hi=mid
        else: lo=mid
    return _greedy(draw,words,fnt,best)

def render_pin(template, bold, light, photos, dark=False, pale=False):
    base = Image.new("RGBA",(W,H),(0,0,0,255))
    base.paste(cover(photos[0],W,H),(0,0))
    base = gradient_overlay(base, 0.30)
    d = ImageDraw.Draw(base)
    maxw = W-160
    t1,t2 = 90,80
    while True:
        fb = font(PLAYFAIR,t1,700); fl = font(PLAYFAIR,t2,400)
        L1 = wrap(d,bold,fb,maxw); L2 = wrap(d,light,fl,maxw) if light else []
        if (len(L1)<=2 and len(L2)<=2) or t1<=54: break
        t1=int(t1*0.93); t2=int(t2*0.93)
    lh1,lh2 = int(t1*1.12),int(t2*1.12)
    accent = template=="Accent" and light
    accentGap = 34 if accent else 0
    gapMid = 22 if light else 0
    blockH = len(L1)*lh1+accentGap+gapMid+len(L2)*lh2

    if template in ("Title top","Accent"): cy = int(H*0.15)
    elif template=="Title bottom":         cy = int(H*0.80)-blockH
    else:                                   cy = H//2-blockH//2

    padX,padY = 52,40
    widest = max([d.textlength(l,font=fb) for l in L1]+([d.textlength(l,font=fl) for l in L2] if L2 else [0]))
    panelW = min(W-48,int(widest)+2*padX)
    bx0=(W-panelW)//2; bx1=(W+panelW)//2
    box=(bx0,max(0,cy-padY),bx1,min(H,cy+blockH+padY))

    mean = base.crop(box).convert("L").resize((1,1)).getpixel((0,0))
    a = max(0.0,min(0.58,(mean-70)/150))
    if dark: a = max(0.58,min(0.82,(mean-20)/150))
    elif pale: a = min(a,0.26)

    base = Image.alpha_composite(base, rrect_layer(box,(0,0,0,int(a*255))))
    base = Image.alpha_composite(base, rrect_layer(box,(242,239,234,38)))
    d = ImageDraw.Draw(base)

    fg = Image.new("RGBA",(W,H),(0,0,0,0)); fd = ImageDraw.Draw(fg)
    y = cy
    for ln in L1:
        fd.text((W//2,y),ln,font=fb,fill=WHITE,anchor="ma"); y+=lh1
    if accent:
        dw = int(min(130,maxw*0.32))
        ImageDraw.Draw(base).rectangle((W//2-dw//2,y+16-accentGap+16,W//2+dw//2,y+16-accentGap+21),fill=TERRA)
        y+=accentGap
    elif light: y+=gapMid
    for ln in L2:
        fd.text((W//2,y),ln,font=fl,fill=WHITE,anchor="ma"); y+=lh2
    fd.text((W//2,H-96),"  ".join("www.milesandflavors.com"),font=font(INTER,30,500),fill=WHITE,anchor="ma")

    sh = Image.new("RGBA",(W,H),(0,0,0,0))
    sh.putalpha(fg.split()[3].point(lambda a2:int(a2*0.6)))
    sh = sh.filter(ImageFilter.GaussianBlur(5))
    base = Image.alpha_composite(base,sh)
    base = Image.alpha_composite(base,fg)
    return base.convert("RGB")

# ── CSV betöltés ─────────────────────────────────────────────────────────────
rows = list(csv.reader(open(PINS,encoding="utf-8-sig"),delimiter=";"))
head = rows[0]; col = {n:i for i,n in enumerate(head)}
pin_data = {}
for r in rows[1:]:
    slug = r[col["URL"]].replace("https://milesandflavors.com/","").strip("/")
    pin_data[(slug, r[col["Pin #"]])] = r

overrides = json.load(open(OVR,encoding="utf-8")) if os.path.exists(OVR) else {}

# ── Fő loop ──────────────────────────────────────────────────────────────────
ok, skip = 0, 0
for slug, pin_no, tmpl, dark, pale, photo_ovr in CORRECTIONS:
    r = pin_data.get((slug, pin_no))
    if not r:
        print(f"SKIP (nincs CSV): {slug} pin{pin_no}"); skip+=1; continue

    bold  = r[col["Pin bold (vastag)"]]
    light = r[col["Pin light (vekony)"]]

    # done/-ban meglévő fájl keresése
    pattern = os.path.join(DONE, f"*{slug}_pin{pin_no}.png")
    existing = glob.glob(pattern)
    if not existing:
        print(f"SKIP (nincs done fájl): {slug} pin{pin_no}"); skip+=1; continue
    out_path = existing[0]

    # fotó kiválasztás
    files = imgs_in(os.path.join(IMG, slug))
    if not files:
        print(f"SKIP (nincs fotó): {slug}"); skip+=1; continue

    if photo_ovr:
        chosen = os.path.join(IMG, slug, photo_ovr)
        if not os.path.exists(chosen):
            print(f"SKIP (fotó nem található: {photo_ovr}): {slug}"); skip+=1; continue
    else:
        okey = f"{slug}_pin{pin_no}"
        if okey in overrides:
            ov = os.path.join(IMG, slug, overrides[okey])
            chosen = ov if os.path.exists(ov) else files[(int(pin_no)-1)%len(files)]
        else:
            chosen = files[(int(pin_no)-1)%len(files)]

    photos = [load(chosen)]
    img = render_pin(tmpl, bold, light, photos, dark=dark, pale=pale)
    img.save(out_path, "PNG")
    print(f"OK [{tmpl}{' dark' if dark else ' pale' if pale else ''}]: {os.path.basename(out_path)}")
    ok+=1

print(f"\nKész: {ok} pin javítva, {skip} kihagyva.")
