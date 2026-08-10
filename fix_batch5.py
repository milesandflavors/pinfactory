# -*- coding: utf-8 -*-
import csv, sys, os
sys.stdout.reconfigure(encoding='utf-8')
PINS = r"D:\Travel blog\PinFactory\pins.csv"
rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]; col = {name: i for i, name in enumerate(head)}

FOTO = {
    ("3-days-in-rome-itinerary", "6"):               "6",   # redd-francisco = uj utcas golden hour
    ("chicago-bucket-list", "6"):                    "9",   # dominique-caron = kajás kep
}

changed = []
for r in rows[1:]:
    if not r or not r[col["URL"]].startswith("http"): continue
    url = r[col["URL"]].lower(); pin = r[col["Pin #"]].strip()
    for (ku, kp), val in FOTO.items():
        if kp == pin and ku in url:
            old = r[col["Foto"]]
            r[col["Foto"]] = val
            print(f"Foto: {r[col['Cikk']]} #{pin}: {old} -> {val}")
            changed.append(r); break

with open(PINS, "w", encoding="utf-8-sig", newline="") as f:
    csv.writer(f, delimiter=";").writerows(rows)

sys.path.insert(0, os.path.dirname(PINS))
import render
for r in changed:
    result = render.render_one(r, col)
    print("OK:", result)
print("Kesz!")

