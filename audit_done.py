"""
Audit done/ mappa:
- Megkeresi a mai naptól (2026-06-21) ütemezett pineket
- Megmutatja mi van done/-ban de nincs scheduled (régi/felesleges)
- Megmutatja mi scheduled de hiányzik done/-ból
"""
import csv, os, glob
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DONE = os.path.join(ROOT, "done")
PINS = os.path.join(ROOT, "pins.csv")
TODAY = datetime(2026, 6, 21)

rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]; col = {n:i for i,n in enumerate(head)}

# Jövőbeli (ma+) pinek
future = []
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
        fname = f"{slug}_pin{pin_no}.png"
        future.append((dt, r[col["Idopont"]], fname, r[col["Pin bold (vastag)"]][:45]))

future.sort()

# Fájlok done/-ban
done_files = set(os.path.basename(f) for f in glob.glob(os.path.join(DONE, "*.png")))
future_fnames = set(f for _, _, f, _ in future)

print(f"=== ÜTEMEZETT (ma+): {len(future)} pin ===")
for dt, t, f, bold in future[:10]:
    status = "OK" if f in done_files else "HIÁNYZIK"
    print(f"  {dt.strftime('%m.%d')} {t}  [{status}]  {bold}  -> {f}")
if len(future) > 10:
    print(f"  ... és még {len(future)-10} db")

print(f"\n=== DONE/-BAN DE NEM ÜTEMEZETT (régi): {len(done_files - future_fnames)} fájl ===")
old = sorted(done_files - future_fnames)
for f in old[:20]:
    print(f"  {f}")
if len(old) > 20:
    print(f"  ... és még {len(old)-20} db")

print(f"\nÖsszesen done/-ban: {len(done_files)} fájl")
print(f"Ebből aktuális (jövőbeli): {len(done_files & future_fnames)}")
print(f"Régi/felesleges: {len(done_files - future_fnames)}")
