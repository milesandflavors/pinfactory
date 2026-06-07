# -*- coding: utf-8 -*-
"""Fine-tune pass: reduce 'first-timer' hook repetition by swapping ~12 formulaic
'First time in X?' hooks to other winning families, and varying ~12 repetitive light lines.
For the 12 swapped pins, also realign title + description to the new angle (shorter, front-loaded)."""
import csv, os

# (Cikk, Pin#) -> (new bold, new light)
HOOKS = {
 # --- 12 full swaps (away from "First time in X?") ---
 ("12-Day Greece Itinerary", 4): ("The biggest Greece mistakes to avoid", "and what to do instead"),
 ("2 Days in Athens", 5): ("What most visitors get wrong in Athens", "and how to do it right"),
 ("25 Best Things to Do in NYC", 2): ("NYC without the overwhelm", "where to start"),
 ("3 Days in Amsterdam", 3): ("Amsterdam without the crowds", "where locals actually go"),
 ("3 Days in Chicago", 3): ("Before you book Chicago", "read this first"),
 ("3 Days in Rome Itinerary (VERIFY SLUG)", 2): ("The Rome mistakes to avoid", "and what to skip"),
 ("4 Days in Barcelona", 4): ("Barcelona without the crowds", "where locals actually go"),
 ("5-Day New York City Itinerary", 3): ("The biggest NYC mistakes to avoid", "what to know before you go"),
 ("7 Days in Marsa Alam", 3): ("Marsa Alam without the guesswork", "how to plan the week"),
 ("Amalfi Coast 5-Day Itinerary", 6): ("Before you book the Amalfi Coast", "read this first"),
 ("Amalfi Coast Bucket List", 5): ("Amalfi Coast: worth it or overrated?", "an honest take"),
 ("Japan 10-Day Itinerary", 2): ("The Japan mistakes to avoid", "what I'd plan differently"),
 # --- 12 light-line varies (keep the strong bold) ---
 ("2 Days in Athens", 1): ("The perfect 2 days in Athens", "mapped so it actually flows"),
 ("3 Days in Chicago", 1): ("The perfect 3 days in Chicago", "day by day, done right"),
 ("3 Days in Rome Itinerary (VERIFY SLUG)", 1): ("The perfect 3 days in Rome", "the route that flows"),
 ("5-Day New York City Itinerary", 1): ("The perfect 5 days in NYC", "no wasted steps"),
 ("Amalfi Coast 5-Day Itinerary", 1): ("The perfect 5 days on the Amalfi Coast", "the perfect plan, day by day"),
 ("Where to Stay in NYC (NEW)", 1): ("Where to stay in NYC", "the best neighborhoods compared"),
 ("Where to Stay in Chicago", 1): ("Where to stay in Chicago", "the best areas compared"),
 ("Where to Stay in Rome (NEW)", 1): ("Where to stay in Rome", "by neighborhood, honestly"),
 ("Where to Stay in Tokyo", 1): ("Where to stay in Tokyo", "the best areas compared"),
 ("Where to Stay in the Dolomites", 1): ("Where to stay in the Dolomites", "the best base for your trip"),
 ("Amsterdam Bucket List", 1): ("The Amsterdam bucket list", "what's actually worth it"),
 ("Best Things to Do in Tokyo", 1): ("The best things to do in Tokyo", "ranked honestly"),
}

# (Cikk, Pin#) -> (new title, new description) for the 12 swapped pins (angle realigned, front-loaded, shorter)
SWAP_META = {
 ("12-Day Greece Itinerary", 4): ("12-Day Greece Itinerary: Mistakes to Avoid",
   "Too many islands, bad ferry timing, only chasing Santorini: the mistakes that wreck a first Greece trip, and the 12-day route that avoids them. Athens, the islands and the beaches, done right."),
 ("2 Days in Athens", 5): ("2 Days in Athens: What Most Visitors Get Wrong",
   "Treating Athens as a one-day stopover, climbing the Acropolis at noon, eating by the sights: what most visitors get wrong, and the 2-day plan that fixes it. Acropolis, Plaka and the best food."),
 ("25 Best Things to Do in NYC", 2): ("Best Things to Do in NYC: Where to Start",
   "New York is huge, so where do you start? The must-dos that matter most: Central Park, the Brooklyn Bridge, the skyline views and the food, plus what you can happily skip on a first trip."),
 ("3 Days in Amsterdam", 3): ("3 Days in Amsterdam: Beyond the Crowds",
   "Past the Dam Square crush: the quiet canals, the Jordaan backstreets and the cafes locals actually use, woven into a 3-day Amsterdam plan with the canals, museums and bikes."),
 ("3 Days in Chicago", 3): ("3 Days in Chicago: Read This Before You Book",
   "What to book ahead, where to stay, and what's actually worth it before you plan Chicago: the architecture cruise, the Bean, deep dish and the lakefront, in a 3-day plan that flows."),
 ("3 Days in Rome Itinerary (VERIFY SLUG)", 2): ("3 Days in Rome: Mistakes to Avoid",
   "Midday at the Colosseum, eating by the Trevi, skipping Trastevere: the Rome mistakes that cost you time, and the 3-day route that avoids them. Colosseum, Vatican and Pantheon, done right."),
 ("4 Days in Barcelona", 4): ("4 Days in Barcelona: Beyond the Crowds",
   "Past Las Ramblas: the Gracia squares, El Born bars and the Bunkers del Carmel sunset locals love, woven into a 4-day Barcelona plan with Sagrada Familia, Park Guell and the beach."),
 ("5-Day New York City Itinerary", 3): ("5 Days in NYC: Mistakes to Avoid",
   "Cramming Midtown, buying every attraction pass, skipping the boroughs: the New York mistakes to avoid, and the 5-day plan that gets it right. The icons, the neighborhoods, the views and the food."),
 ("7 Days in Marsa Alam", 3): ("7 Days in Marsa Alam: How to Plan the Week",
   "Which reefs, which trips, how much beach time: how to plan a week in Marsa Alam without the guesswork. Snorkeling, a dolphin reef, a desert safari and pure Red Sea rest, day by day."),
 ("Amalfi Coast 5-Day Itinerary", 6): ("5 Days on the Amalfi Coast: Before You Book",
   "Where to base, how the ferries work, which towns to prioritize: what to know before you book the Amalfi Coast, plus the 5-day plan that ties Positano, Ravello and Capri together."),
 ("Amalfi Coast Bucket List", 5): ("Amalfi Coast Bucket List: Worth It or Overrated?",
   "An honest take on the Amalfi hype: which experiences earn the trip and which to skip. Positano, Ravello, the Path of the Gods, a Capri day and the boat trips, ranked by what's truly worth it."),
 ("Japan 10-Day Itinerary", 2): ("Japan 10-Day Itinerary: Mistakes to Avoid",
   "Over-packing the route, skipping the JR Pass math, too long in Tokyo: the Japan mistakes to avoid, and the 10-day plan I'd do again. Tokyo, Kyoto, Osaka and a Mt Fuji day, balanced."),
}

ROOT = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.reader(open(os.path.join(ROOT, "pins.csv"), encoding="utf-8-sig"), delimiter=";"))
h = {n: i for i, n in enumerate(rows[0])}
nh = nm = 0
for r in rows[1:]:
    k = (r[h["Cikk"]], int(r[h["Pin #"]]))
    if k in HOOKS:
        b, l = HOOKS[k]; r[h["Pin bold (vastag)"]] = b; r[h["Pin light (vekony)"]] = l; nh += 1
    if k in SWAP_META:
        t, d = SWAP_META[k]; r[h["Pin cim"]] = t; r[h["Pin leiras"]] = d; nm += 1
with open(os.path.join(ROOT, "pins.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(rows[0]); w.writerows(rows[1:])
print(f"Hooks changed: {nh} | titles+descriptions realigned: {nm}")

# verify counts
import re
ft = re.compile(r"first[- ]?time", re.I)
hook_ft = sum(1 for r in rows[1:] if ft.search(r[h["Pin bold (vastag)"]] + " " + r[h["Pin light (vekony)"]]))
print(f"'first-time(r)' in HOOKS now: {hook_ft} (was 42)")
