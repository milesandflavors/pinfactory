# -*- coding: utf-8 -*-
"""Apply review pass 1: per-pin box position/opacity (Template column) changes."""
import csv, os

# (slug, pin#) -> new Template
CH = {
 ("barcelona-bucket-list", "1"): "Title bottom light",
 ("how-to-book-hotels-like-a-pro", "1"): "Title top light",
 ("best-day-trips-from-amsterdam", "1"): "Title bottom",
 ("best-beaches-in-zakynthos", "1"): "Title bottom",
 ("marsa-alam-travel-costs", "1"): "Title bottom",
 ("where-to-stay-on-the-amalfi-coast", "1"): "Title top light",
 ("best-things-to-do-in-osaka", "1"): "Title bottom",
 ("where-to-stay-in-amsterdam", "1"): "Title bottom",
 ("esim-for-travel", "1"): "Title bottom",
 ("3-days-in-rome-itinerary", "2"): "Title bottom dark",
 ("12-day-greece-itinerary", "2"): "Title top",
 ("5-days-on-the-amalfi-coast-itinerary", "2"): "Title top",
 ("4-days-in-barcelona-the-perfect-itinerary", "2"): "Title top",
 ("2-days-in-athens", "2"): "Title top",
 ("chicago-bucket-list-25-best-things-to-do", "2"): "Title top",
 ("japan-10-day-itinerary", "2"): "Centered light",
 ("how-to-find-cheap-flights", "2"): "Title top light",
 ("best-things-to-do-in-tokyo", "2"): "Title top",
 ("barcelona-bucket-list", "2"): "Title top light",
 ("5-day-new-york-city-itinerary", "2"): "Title top",
 ("best-day-trips-from-amsterdam", "2"): "Title top",
 ("best-things-to-do-in-rome", "2"): "Title top",
 ("where-to-stay-in-chicago-7-best-areas-hotels", "2"): "Title bottom",
 ("marsa-alam-travel-costs", "2"): "Title top",
 ("day-trip-to-the-dolomites-from-venice", "1"): "Title bottom",
 ("best-things-to-do-in-osaka", "2"): "Title top",
 ("3-days-in-rome-itinerary", "3"): "Title top",
 ("best-canal-cruises-in-amsterdam", "1"): "Title bottom",
 ("12-day-greece-itinerary", "3"): "Centered",
 ("5-days-on-the-amalfi-coast-itinerary", "3"): "Centered",
 ("best-travel-money-card", "3"): "Title top",
 ("where-to-stay-on-the-amalfi-coast", "2"): "Title top",
 ("3-days-in-amsterdam", "3"): "Title bottom dark",
 ("how-to-find-cheap-flights", "3"): "Title top dark",
 ("best-things-to-do-in-tokyo", "3"): "Title top",
}

ROOT = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.reader(open(os.path.join(ROOT, "pins.csv"), encoding="utf-8-sig"), delimiter=";"))
h = {n: i for i, n in enumerate(rows[0])}
n = 0
seen = set()
for r in rows[1:]:
    slug = r[h["URL"]].replace("https://milesandflavors.com/", "").strip("/")
    key = (slug, r[h["Pin #"]])
    if key in CH:
        r[h["Template"]] = CH[key]; n += 1; seen.add(key)
with open(os.path.join(ROOT, "pins.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(rows[0]); w.writerows(rows[1:])
print("Applied:", n, "of", len(CH))
missing = set(CH) - seen
if missing:
    print("NOT FOUND:", missing)
