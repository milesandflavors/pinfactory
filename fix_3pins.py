# -*- coding: utf-8 -*-
"""Foto override + re-render: Sao Miguel #2, Amalfi 5-Day #5 (URL alapu matcheles)"""
import csv, sys, os

PINS = r"D:\Travel blog\PinFactory\pins.csv"

# (url_reszlet, pin_szam) -> foto_index
FOTO_NEW = {
    ("sao-miguel", "2"): "4",
    ("5-days-on-the-amalfi-coast", "5"): "8",
}

rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]
col  = {name: i for i, name in enumerate(head)}

changed = []
for r in rows[1:]:
    if not r or not r[col["URL"]].startswith("http"): continue
    url    = r[col["URL"]].lower()
    pin_no = r[col["Pin #"]].strip()
    for (key_url, key_pin), foto_val in FOTO_NEW.items():
        if key_pin == pin_no and key_url in url:
            r[col["Foto"]] = foto_val
            changed.append(r)
            print(f"Foto: {r[col['Cikk']]} #{pin_no} -> {foto_val}")
            break

with open(PINS, "w", encoding="utf-8-sig", newline="") as f:
    csv.writer(f, delimiter=";").writerows(rows)
print(f"{len(changed)} sor frissitve")

sys.path.insert(0, os.path.dirname(PINS))
import render
for r in changed:
    render.render_one(r, col)
print("Kesz!")

