"""
A done/-ban lévő slug_pinN.png fájlokat átnevezi:
  YYYY.MM.DD_HH-MM_slug_pinN.png
a pins.csv ütemezés alapján.
"""
import csv, os, glob
from datetime import datetime

ROOT  = os.path.dirname(os.path.abspath(__file__))
DONE  = os.path.join(ROOT, "done")
PINS  = os.path.join(ROOT, "pins.csv")
TODAY = datetime(2026, 6, 21)

rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]; col = {n:i for i,n in enumerate(head)}

# Összes jövőbeli pin dátum-mapje: fname -> dátum_idő prefix
scheduled = {}
for r in rows[1:]:
    if not r or not r[col["URL"]].startswith("http"): continue
    d = r[col["Datum"]].strip()
    if not d: continue
    try:
        dt = datetime.strptime(d, "%Y.%m.%d")
    except:
        continue
    if dt >= TODAY:
        slug = r[col["URL"]].replace("https://milesandflavors.com/","").strip("/")
        pin_no = r[col["Pin #"]]
        old_name = f"{slug}_pin{pin_no}.png"
        t = r[col["Idopont"]].strip().replace(":", "-")
        prefix = dt.strftime("%Y.%m.%d") + f"_{t}"
        new_name = f"{prefix}_{slug}_pin{pin_no}.png"
        scheduled[old_name] = new_name

renamed = 0
skipped = 0
for fpath in sorted(glob.glob(os.path.join(DONE, "*.png"))):
    fname = os.path.basename(fpath)
    if fname in scheduled:
        new_path = os.path.join(DONE, scheduled[fname])
        os.rename(fpath, new_path)
        renamed += 1
    else:
        skipped += 1
        print(f"  [SKIP] {fname}")

print(f"\nÁtnevezve: {renamed} fájl")
if skipped:
    print(f"Nem találtam pins.csv-ben: {skipped} fájl")
