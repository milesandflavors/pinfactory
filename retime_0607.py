# -*- coding: utf-8 -*-
"""Re-time the 06.07 pins to 9:00-15:00 hourly (keeping current order),
and rename the matching done/ PNGs so filenames stay accurate (no re-render = no duplicates)."""
import csv, os, datetime, glob

ROOT = os.path.dirname(os.path.abspath(__file__))
NEW_TIMES = ["9:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00"]
DAY = "2026.06.07"

rows = list(csv.reader(open(os.path.join(ROOT, "pins.csv"), encoding="utf-8-sig"), delimiter=";"))
h = {n: i for i, n in enumerate(rows[0])}

# collect 06.07 rows, sort by real time
day = [r for r in rows[1:] if r[h["Datum"]] == DAY]
day.sort(key=lambda r: datetime.datetime.strptime(r[h["Idopont"]], "%H:%M"))
assert len(day) == len(NEW_TIMES), f"expected {len(NEW_TIMES)} pins, found {len(day)}"

for r, newt in zip(day, NEW_TIMES):
    oldt = r[h["Idopont"]]
    slug = r[h["URL"]].replace("https://milesandflavors.com/", "").strip("/")
    pin = r[h["Pin #"]]
    # rename the rendered PNG if present
    old_png = os.path.join(ROOT, "done", f"{DAY}_{oldt.replace(':','-')}_{slug}_pin{pin}.png")
    new_png = os.path.join(ROOT, "done", f"{DAY}_{newt.replace(':','-')}_{slug}_pin{pin}.png")
    if os.path.exists(old_png) and old_png != new_png:
        os.replace(old_png, new_png)
        tag = "renamed img"
    elif os.path.exists(new_png):
        tag = "img already named"
    else:
        tag = "NO IMG"
    r[h["Idopont"]] = newt
    print(f"  {oldt:>5} -> {newt:<5} {tag:18} {r[h['Cikk']]}")

with open(os.path.join(ROOT, "pins.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(rows[0]); w.writerows(rows[1:])
print("Done.")
