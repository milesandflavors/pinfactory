# -*- coding: utf-8 -*-
import csv, sys, os
sys.stdout.reconfigure(encoding='utf-8')
PINS = r"D:\Travel blog\PinFactory\pins.csv"
rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]; col = {name: i for i, name in enumerate(head)}

TMPL = {
    ("20-free-things-to-do-in-chicago", "1"):        "Centered",
    ("chicago-architecture-river-cruise", "3"):       "Title top",
    ("best-beaches-in-zakynthos", "6"):               "Title top",
}
FOTO = {
    ("3-days-in-rome-itinerary", "6"): "1",  # cristina-gottardi = Trastevere utca
}

changed = []
for r in rows[1:]:
    if not r or not r[col["URL"]].startswith("http"): continue
    url = r[col["URL"]].lower(); pin = r[col["Pin #"]].strip()
    mod = False
    for (ku, kp), val in TMPL.items():
        if kp == pin and ku in url:
            old = r[col["Template"]]
            r[col["Template"]] = val
            print(f"Tmpl: {r[col['Cikk']]} #{pin}: '{old}' -> '{val}'")
            mod = True; break
    for (ku, kp), val in FOTO.items():
        if kp == pin and ku in url:
            old = r[col["Foto"]]
            r[col["Foto"]] = val
            print(f"Foto: {r[col['Cikk']]} #{pin}: {old} -> {val}")
            mod = True; break
    if mod: changed.append(r)

with open(PINS, "w", encoding="utf-8-sig", newline="") as f:
    csv.writer(f, delimiter=";").writerows(rows)

sys.path.insert(0, os.path.dirname(PINS))
import render
for r in changed:
    result = render.render_one(r, col)
    print("OK:", result)
print("Kesz!")

