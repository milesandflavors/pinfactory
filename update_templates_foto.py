# -*- coding: utf-8 -*-
"""
Template pozíció változások + Foto képindex override-ok a pins.csv-be.
Futtatás: python update_templates_foto.py
"""
import csv, shutil, os
from datetime import datetime

PINS = r"D:\Travel blog\PinFactory\pins.csv"
backup = PINS.replace(".csv", f"_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
shutil.copy2(PINS, backup)
print(f"Backup: {backup}")

# --- Template változások: (cikk_részlet, pin_szam) -> uj_template ---
# cikk_részlet = kis/nagybetű mindegy, tartalmaz keresés
TEMPLATE_CHANGES = {
    ("montserrat day trip", "1"):              "Title bottom light",
    ("best day trips from amsterdam", "4"):    "Centered",
    ("zakynthos road trip", "1"):              "Title bottom",
    ("where to stay in barcelona", "4"):       "Centered",
    ("chicago travel costs", "1"):             "Title bottom",
    ("where to stay in chicago", "4"):         "Centered",
    ("azores whale watching", "2"):            "Title top dark",
    ("montserrat day trip", "2"):              "Title top dark",
    ("best things to do in rome (new)", "5"):  "Title bottom",
    ("nyc travel costs", "1"):                 "Title bottom",
    ("where to stay on the amalfi coast", "5"):"Title top dark",
    ("chicago architecture river cruise", "3"):"Centered dark",
}

# --- Foto override-ok: (cikk_részlet, pin_szam) -> foto_index (1-alapú) ---
FOTO_OVERRIDES = {
    # Amalfi BL #4: cathedral helyett coastal driving kép (idx 4 = 5. kép)
    ("amalfi coast bucket list", "4"): "5",
    # Amalfi BL #6: 1. naplementes kép (jordi, idx 7 = 8. kép)
    ("amalfi coast bucket list", "6"): "8",
    # Amalfi BL #7: 2. naplementes kép (yianni, idx 9 = 10. kép)
    ("amalfi coast bucket list", "7"): "10",
    # Chicago BL #6: Navy Pier helyett oroszlán szobor (idx 6 = 7. kép)
    ("chicago bucket list", "6"): "7",
    # Amsterdam Canal #3: getty canal kép, nem szárazföldi ház (idx 0 = 1. kép)
    ("best canal cruises in amsterdam", "3"): "1",
}

def matches(cikk_val, key_part):
    return key_part in cikk_val.lower()

rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]
col  = {name: i for i, name in enumerate(head)}

# Foto oszlop hozzáadása ha nincs
if "Foto" not in col:
    head.append("Foto")
    col["Foto"] = len(head) - 1
    for r in rows[1:]:
        r.append("")
    print("Foto oszlop hozzáadva")

template_changes = 0
foto_changes = 0

for r in rows[1:]:
    if not r or not r[col["URL"]].startswith("http"):
        continue
    cikk   = r[col["Cikk"]].strip()
    pin_no = r[col["Pin #"]].strip()

    # Template update
    for (key_cikk, key_pin), new_tmpl in TEMPLATE_CHANGES.items():
        if key_pin == pin_no and matches(cikk, key_cikk):
            old = r[col["Template"]]
            r[col["Template"]] = new_tmpl
            print(f"  Template: {cikk} #{pin_no}: '{old}' -> '{new_tmpl}'")
            template_changes += 1
            break

    # Foto override
    for (key_cikk, key_pin), foto_val in FOTO_OVERRIDES.items():
        if key_pin == pin_no and matches(cikk, key_cikk):
            r[col["Foto"]] = foto_val
            print(f"  Foto: {cikk} #{pin_no} -> {foto_val}")
            foto_changes += 1
            break

# Mentés
with open(PINS, "w", encoding="utf-8-sig", newline="") as f:
    csv.writer(f, delimiter=";").writerows(rows)

print(f"\nKész! {template_changes} Template + {foto_changes} Foto változtatás → {PINS}")

