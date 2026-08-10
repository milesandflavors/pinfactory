"""
Régi (nem ütemezett) pineket áthelyezi done/ -> done_archive/
A done/-ban csak az aktuális, jövőbeli pinek maradnak.
"""
import csv, os, glob, shutil
from datetime import datetime

ROOT    = os.path.dirname(os.path.abspath(__file__))
DONE    = os.path.join(ROOT, "done")
ARCHIVE = os.path.join(ROOT, "done_archive")
PINS    = os.path.join(ROOT, "pins.csv")
TODAY   = datetime(2026, 6, 21)

os.makedirs(ARCHIVE, exist_ok=True)

rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]; col = {n:i for i,n in enumerate(head)}

future_fnames = set()
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
        future_fnames.add(f"{slug}_pin{r[col['Pin #']]}.png")

done_files = glob.glob(os.path.join(DONE, "*.png"))
moved = 0
for f in done_files:
    fname = os.path.basename(f)
    if fname not in future_fnames:
        shutil.move(f, os.path.join(ARCHIVE, fname))
        moved += 1

print(f"Archivált: {moved} régi pin -> done_archive/")
remaining = len(glob.glob(os.path.join(DONE, "*.png")))
print(f"Done/-ban maradt: {remaining} aktuális pin")
