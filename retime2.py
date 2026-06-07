# -*- coding: utf-8 -*-
"""Re-time the 06.07 pins to the new afternoon/evening split, keeping current order.
Renames the matching done/ PNGs (no re-render = no duplicates)."""
import csv, os, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DAY = "2026.06.07"
NEW_TIMES = ["13:45", "14:00", "14:30", "20:00", "21:00", "22:00", "23:00"]

rows = list(csv.reader(open(os.path.join(ROOT, "pins.csv"), encoding="utf-8-sig"), delimiter=";"))
h = {n: i for i, n in enumerate(rows[0])}
day = [r for r in rows[1:] if r[h["Datum"]] == DAY]
day.sort(key=lambda r: datetime.datetime.strptime(r[h["Idopont"]], "%H:%M"))
assert len(day) == len(NEW_TIMES), f"expected {len(NEW_TIMES)}, found {len(day)}"

for r, newt in zip(day, NEW_TIMES):
    oldt = r[h["Idopont"]]
    slug = r[h["URL"]].replace("https://milesandflavors.com/", "").strip("/")
    pin = r[h["Pin #"]]
    old_png = os.path.join(ROOT, "done", f"{DAY}_{oldt.replace(':','-')}_{slug}_pin{pin}.png")
    new_png = os.path.join(ROOT, "done", f"{DAY}_{newt.replace(':','-')}_{slug}_pin{pin}.png")
    if os.path.exists(old_png) and old_png != new_png:
        os.replace(old_png, new_png); tag = "img renamed"
    elif os.path.exists(new_png):
        tag = "img ok"
    else:
        tag = "NO IMG"
    r[h["Idopont"]] = newt
    print(f"  {oldt:>5} -> {newt:<5} {tag:12} {r[h['Cikk']]}")

with open(os.path.join(ROOT, "pins.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(rows[0]); w.writerows(rows[1:])
print("Done.")
