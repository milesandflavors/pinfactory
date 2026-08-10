# -*- coding: utf-8 -*-
"""Re-render the batch2 affected pins by date range."""
import csv, sys, os

PINS = r"D:\Travel blog\PinFactory\pins.csv"
TODAY = "2026.06.23"
END   = "2026.07.04"

rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]; col = {name: i for i, name in enumerate(head)}

sys.path.insert(0, os.path.dirname(PINS))
import render

made = skip = 0
for r in rows[1:]:
    if not r or not r[col["URL"]].startswith("http"): continue
    datum = r[col["Datum"]].strip()
    if not (TODAY <= datum <= END): continue
    try:
        result = render.render_one(r, col)
        if result: made += 1
    except Exception as e:
        print(f"  HIBA: {r[col['Cikk']]} #{r[col['Pin #']]} - {e}")
        skip += 1

print(f"\nKesz! {made} OK, {skip} hiba.")

