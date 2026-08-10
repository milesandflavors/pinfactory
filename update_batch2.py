# -*- coding: utf-8 -*-
"""Batch 2: Template + Foto valtozasok, majd re-render az erintett pinekre."""
import csv, sys, os, shutil
from datetime import datetime

PINS = r"D:\Travel blog\PinFactory\pins.csv"
backup = PINS.replace(".csv", f"_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")
shutil.copy2(PINS, backup)

# (url_reszlet, pin_szam) -> uj Template
TEMPLATE_CHANGES = {
    ("hakone-day-trip", "1"):                    "Centered",
    ("where-to-stay-on-the-amalfi-coast", "3"):  "Title top",
    ("where-to-stay-in-amsterdam", "4"):          "Accent dark",
    ("best-canal-cruises-in-amsterdam", "2"):     "Centered dark",
    ("where-to-stay-in-chicago", "4"):            "Centered dark",
    ("barcelona-travel-costs", "1"):              "Centered",
    ("azores-whale-watching", "2"):               "Title top",       # volt "dark" - tul sotet
    ("free-stopover-flights", "2"):               "Title top",
    ("where-to-stay-in-rome", "2"):               "Title top",
    ("where-to-stay-in-tokyo", "1"):              "Title bottom",
    ("montserrat-day-trip", "2"):                 "Title bottom",    # user visszavonta a top dark-ot
    ("best-beaches-in-zakynthos", "5"):           "Title bottom",
    ("best-things-to-do-in-rome", "5"):           "Title bottom dark",
    ("amalfi-coast-travel-costs", "1"):           "Title bottom",
    ("rome-travel-costs", "1"):                   "Title bottom",
    ("5-day-new-york-city-itinerary", "5"):       "Title bottom",
    ("where-to-stay-in-barcelona", "5"):          "Title bottom",
    ("best-time-to-visit-the-azores", "3"):       "Title top",
    ("azores-whale-watching", "3"):               "Title top",       # volt "Centered dark" - szoveg takarta a bahna farkat
    ("2-days-in-athens", "6"):                    "Title top",
    ("free-stopover-flights", "3"):               "Title top",
    ("where-to-stay-in-rome", "3"):               "Title bottom dark",
    ("montserrat-day-trip", "3"):                 "Centered",        # volt "light" - kicsit sotetebb kell
    ("amalfi-coast-bucketlist", "6"):             "Title bottom",
    ("where-to-stay-on-the-amalfi-coast", "5"):  "Centered",        # volt "Title top dark"
}

# (url_reszlet, pin_szam) -> Foto index (1-alapu)
FOTO_CHANGES = {
    # Amalfi BL: uj kepek miatt indexek elcsusztak (13 kep most)
    ("amalfi-coast-bucketlist", "4"):  "12",  # reiseuhu = beach (idx 11)
    ("amalfi-coast-bucketlist", "6"):  "9",   # jordi sunset (idx 8, elcsuszott)
    ("amalfi-coast-bucketlist", "7"):  "13",  # yianni sunset (idx 12, elcsuszott)
    # Roma: nappali Colosseum + nem Trastevere
    ("3-days-in-rome-itinerary", "5"): "2",   # getty (idx 1) - nappali?
    ("3-days-in-rome-itinerary", "6"): "3",   # jorgen-hendriksen (idx 2) - nem Trastevere
    # Barcelona ikonikusabb kep
    ("4-days-in-barcelona", "5"):      "4",   # Sagrada Familia (idx 3)
}

rows = list(csv.reader(open(PINS, encoding="utf-8-sig"), delimiter=";"))
head = rows[0]
col  = {name: i for i, name in enumerate(head)}

tmpl_n = foto_n = 0
changed_rows = []

for r in rows[1:]:
    if not r or not r[col["URL"]].startswith("http"): continue
    url    = r[col["URL"]].lower()
    pin_no = r[col["Pin #"]].strip()
    modified = False

    for (key_url, key_pin), new_tmpl in TEMPLATE_CHANGES.items():
        if key_pin == pin_no and key_url in url:
            old = r[col["Template"]]
            if old != new_tmpl:
                r[col["Template"]] = new_tmpl
                print(f"  Tmpl: {r[col['Cikk']]} #{pin_no}: '{old}' -> '{new_tmpl}'")
                tmpl_n += 1; modified = True
            break

    for (key_url, key_pin), foto_val in FOTO_CHANGES.items():
        if key_pin == pin_no and key_url in url:
            old = r[col["Foto"]]
            if old != foto_val:
                r[col["Foto"]] = foto_val
                print(f"  Foto: {r[col['Cikk']]} #{pin_no}: {old} -> {foto_val}")
                foto_n += 1; modified = True
            break

    if modified:
        changed_rows.append(r)

with open(PINS, "w", encoding="utf-8-sig", newline="") as f:
    csv.writer(f, delimiter=";").writerows(rows)
print(f"\n{tmpl_n} Template + {foto_n} Foto valtozas mentve.")

# Re-render csak az erintett pineket
sys.path.insert(0, os.path.dirname(PINS))
import render
made = 0
for r in changed_rows:
    result = render.render_one(r, col)
    if result: made += 1

# 20-free-things Chicago #1 ujrarenderelese (lion kep masolva)
for r in rows[1:]:
    if not r or not r[col["URL"]].startswith("http"): continue
    if "20-free-things-to-do-in-chicago" in r[col["URL"]].lower() and r[col["Pin #"]].strip() == "1":
        result = render.render_one(r, col)
        if result: made += 1
        break

print(f"\nKesz! {made} pin ujrarenderelve.")

