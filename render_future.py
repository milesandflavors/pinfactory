# -*- coding: utf-8 -*-
"""Csak a mai dátumtól kezdve a jövőbeni pineket rendereli újra."""
import csv, os, sys, subprocess
from datetime import datetime

PINS = r"D:\Travel blog\PinFactory\pins.csv"
TODAY = datetime.now().strftime("%Y.%m.%d")

rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]
col  = {name: i for i, name in enumerate(head)}

future = []
for r in rows[1:]:
    if not r or not r[col["URL"]].startswith("http"): continue
    datum = r[col["Datum"]].strip() if "Datum" in col else ""
    ido   = r[col["Idopont"]].strip() if "Idopont" in col else ""
    if datum >= TODAY:
        future.append((datum, ido, r))

print(f"Jövőbeni pinek: {len(future)}")

# render.py importálása és futtatása
sys.path.insert(0, os.path.dirname(PINS))
import render

made = 0
for datum, ido, r in future:
    result = render.render_one(r, col)
    if result:
        made += 1
        sys.stdout.write(f"  OK {made}/{len(future)}: {result}\n")
        sys.stdout.flush()

print(f"\nKesz! {made} pin renderelve.")

