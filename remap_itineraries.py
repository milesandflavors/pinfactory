# -*- coding: utf-8 -*-
"""Split the generic 'Travel Itineraries' board into geographic boards
(Europe / USA / Asia), per the agreed taxonomy."""
import csv, os

MAP = {
 '3 Days in Rome Itinerary (VERIFY SLUG)': 'Europe Travel Itineraries',
 '12-Day Greece Itinerary':               'Europe Travel Itineraries',
 '4 Days in Barcelona':                    'Europe Travel Itineraries',
 'Amalfi Coast 5-Day Itinerary':           'Europe Travel Itineraries',
 'Zakynthos Road Trip Itinerary':          'Europe Travel Itineraries',
 '3 Days in Amsterdam':                    'Europe Travel Itineraries',
 '5-Day New York City Itinerary':          'USA Travel Itineraries',
 '3 Days in Chicago':                      'USA Travel Itineraries',
 'Japan 10-Day Itinerary':                 'Asia Travel Itineraries',
 '7 Days in Marsa Alam':                   'Egypt Travel Guide',
}

ROOT = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.reader(open(os.path.join(ROOT, "pins.csv"), encoding="utf-8-sig"), delimiter=";"))
h = {n: i for i, n in enumerate(rows[0])}
from collections import Counter
cnt = Counter()
for r in rows[1:]:
    if r[h["Board"]].strip() == "Travel Itineraries":
        a = r[h["Cikk"]]
        if a in MAP:
            r[h["Board"]] = MAP[a]; cnt[MAP[a]] += 1
        else:
            cnt["(left as Travel Itineraries) " + a] += 1
with open(os.path.join(ROOT, "pins.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(rows[0]); w.writerows(rows[1:])
for b, n in cnt.most_common():
    print(f"  {n:>2}  {b}")
