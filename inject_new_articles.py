"""
inject_new_articles.py
Beilleszti az 5 új cikk 22 pinjét a meglévő ütemezésbe (jún. 20-tól),
a leggyakoribb cikkek egy-egy pinét kitolva júl. 18 utánra.
Módok: preview (csak megmutatja) | write (tényleg írja a CSV-t)
"""

import csv, shutil, sys, io
from datetime import datetime, timedelta
from collections import Counter

# Force UTF-8 output so special chars (ã, é, etc.) don't crash on Windows cp1250
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CSV_PATH = r'D:\Travel blog\PinFactory\pins.csv'
BACKUP_PATH = r'D:\Travel blog\PinFactory\pins_backup_20260619.csv'

# ── 22 új pin definíció ─────────────────────────────────────────────────────

NEW_PINS = [
    # ── Things to Do in São Miguel (5 pin) ──
    dict(
        Cikk='Things to Do in São Miguel, Azores',
        **{'Pin #': '1'},
        Template='Title top light',
        Photos='1',
        **{'Pin bold (vastag)': 'São Miguel, Azores', 'Pin light (vekony)': "the bucket list nobody talks about"},
        URL='https://milesandflavors.com/things-to-do-in-sao-miguel/',
        Board='Best Things to Do Around the World',
        **{'Pin cim': 'Best Things to Do in São Miguel, Azores (Honestly Ranked)',
           'Pin leiras': "Twin crater lakes, geothermal hot springs that cook your lunch underground, whale watching with one of the highest success rates in the world — and most of Europe has never heard of it. São Miguel is the Azores island that permanently ruins your travel standards. Honestly ranked bucket list: what's genuinely unmissable, what's overhyped, and how to fit it all in.",
           'Alt text': 'The vivid blue-green waters of Sete Cidades twin crater lakes surrounded by rolling green hills in São Miguel, Azores.'}
    ),
    dict(
        Cikk='Things to Do in São Miguel, Azores',
        **{'Pin #': '2'},
        Template='Title bottom dark',
        Photos='1',
        **{'Pin bold (vastag)': 'Sete Cidades', 'Pin light (vekony)': 'the view that redefines "worth it"'},
        URL='https://milesandflavors.com/things-to-do-in-sao-miguel/',
        Board='Europe Travel Itineraries',
        **{'Pin cim': 'Sete Cidades Azores: How to See the Twin Lakes (Without the Crowds)',
           'Pin leiras': "One lake is green. One is blue. Both sit inside an ancient volcanic caldera — and on a clear morning, the view looks like someone dropped a painting into the middle of the Atlantic. How to see Sete Cidades without the tour buses: the viewpoint that's actually worth it, the hike that has it almost to yourself, and what else to do while you're in this corner of São Miguel.",
           'Alt text': 'Panoramic view of the Sete Cidades caldera in São Miguel showing two contrasting colored lakes from the Vista do Rei viewpoint.'}
    ),
    dict(
        Cikk='Things to Do in São Miguel, Azores',
        **{'Pin #': '3'},
        Template='Centered light',
        Photos='1',
        **{'Pin bold (vastag)': 'Furnas, São Miguel', 'Pin light (vekony)': 'hot springs, geysers & the best stew of your life'},
        URL='https://milesandflavors.com/things-to-do-in-sao-miguel/',
        Board='Best Things to Do Around the World',
        **{'Pin cim': 'Furnas Hot Springs São Miguel: What to See, Do & Eat',
           'Pin leiras': "In Furnas, the ground is alive. Geothermal geysers burst out of the earth, thermal pools steam through the forest — and the local stew has been slow-cooking underground in volcanic heat since this morning. This half-day in São Miguel is the one you'll be telling people about for years. Exactly what to do in Furnas, where to eat, and how to fit it into your Azores itinerary.",
           'Alt text': 'Steam rising from the geothermal geysers and boiling mud pools in Furnas village, São Miguel, Azores.'}
    ),
    dict(
        Cikk='Things to Do in São Miguel, Azores',
        **{'Pin #': '4'},
        Template='Title bottom light',
        Photos='1',
        **{'Pin bold (vastag)': 'São Miguel Azores', 'Pin light (vekony)': '3 days, zero regrets'},
        URL='https://milesandflavors.com/things-to-do-in-sao-miguel/',
        Board='Europe Travel Itineraries',
        **{'Pin cim': 'São Miguel Azores Travel Guide: What to Do, See & Skip',
           'Pin leiras': "You book three days in São Miguel. By day two, you're looking up flight extensions. The crater lakes, the thermal pools, the whale watching, the food — this island doesn't ease you in gently, it converts you immediately. Complete São Miguel travel guide: what to prioritize, what to skip, and how many days you actually need to do it justice.",
           'Alt text': 'A winding road through the lush green volcanic landscape of São Miguel island in the Azores with the ocean visible in the distance.'}
    ),
    dict(
        Cikk='Things to Do in São Miguel, Azores',
        **{'Pin #': '5'},
        Template='Accent',
        Photos='1',
        **{'Pin bold (vastag)': "The Azores", 'Pin light (vekony)': "Europe's best-kept secret"},
        URL='https://milesandflavors.com/things-to-do-in-sao-miguel/',
        Board='Bucket list destinations',
        **{'Pin cim': "São Miguel Azores: 15 Things to Do on Portugal's Most Stunning Island",
           'Pin leiras': "The Azores sit in the middle of the Atlantic, technically Europe but feeling like nowhere else on earth. São Miguel has volcanic crater lakes, steaming geysers, year-round whale watching, and prices that remind you travel doesn't have to cost a fortune. This is the bucket list for the island most people are still sleeping on — before everyone else catches up.",
           'Alt text': 'Aerial view of São Miguel island in the Azores showing lush green volcanic hills descending to the deep blue Atlantic ocean.'}
    ),

    # ── Best Time to Visit the Azores (3 pin) ──
    dict(
        Cikk='Best Time to Visit the Azores',
        **{'Pin #': '1'},
        Template='Title top light',
        Photos='1',
        **{'Pin bold (vastag)': 'Best Time to Visit the Azores', 'Pin light (vekony)': "the honest answer (it's not what you expect)"},
        URL='https://milesandflavors.com/best-time-to-visit-the-azores/',
        Board='Europe Travel Itineraries',
        **{'Pin cim': 'Best Time to Visit the Azores: Month-by-Month Honest Guide',
           'Pin leiras': "The travel blogs say summer. They're not wrong — but they're leaving things out. Spring in the Azores means whale watching at its absolute peak, hillsides covered in hydrangeas, and half the crowds. Winter is mild, cheap, and mostly yours. Month-by-month honest guide to the Azores: what each season actually delivers, and the one window most people completely overlook.",
           'Alt text': 'Lush green hillsides of São Miguel, Azores, covered in hydrangeas under partly cloudy Atlantic skies.'}
    ),
    dict(
        Cikk='Best Time to Visit the Azores',
        **{'Pin #': '2'},
        Template='Title bottom dark',
        Photos='1',
        **{'Pin bold (vastag)': 'Azores: Spring vs Summer', 'Pin light (vekony)': 'which season should you book?'},
        URL='https://milesandflavors.com/best-time-to-visit-the-azores/',
        Board='Best Travel Tips & Hacks',
        **{'Pin cim': 'Azores in Spring vs Summer: Which Season Is Actually Better?',
           'Pin leiras': "April in the Azores: whale watching peak, hydrangeas everywhere, a quarter of the August crowds. August: gorgeous, but you'll feel it in the queues and the prices. Both are wonderful — they're just completely different trips. Honest breakdown of every season so you can pick the one that fits your travel style and your budget, not just the one that gets the best Instagram.",
           'Alt text': 'Fields of blue hydrangeas lining the roadsides of São Miguel island in the Azores during spring bloom.'}
    ),
    dict(
        Cikk='Best Time to Visit the Azores',
        **{'Pin #': '3'},
        Template='Centered',
        Photos='1',
        **{'Pin bold (vastag)': 'Visiting the Azores?', 'Pin light (vekony)': "here's when to actually go"},
        URL='https://milesandflavors.com/best-time-to-visit-the-azores/',
        Board='Europe Travel Itineraries',
        **{'Pin cim': 'When to Visit the Azores: Weather, Crowds & Whale Watching Season',
           'Pin leiras': "Yes, the Azores weather is unpredictable. Four seasons in one day is real. But here's what no one tells you: that mist rolling over the crater lakes at 8am is one of the most beautiful things you will ever see — and by noon it's often sunny. Real weather expectations, whale watching season by month, and the windows that give you the best Azores experience for the least amount of money.",
           'Alt text': 'Dramatic misty clouds rolling over the green volcanic peaks of São Miguel island, Azores, with a patch of blue sky above.'}
    ),

    # ── Azores Whale Watching (4 pin) ──
    dict(
        Cikk='Azores Whale Watching',
        **{'Pin #': '1'},
        Template='Title top light',
        Photos='1',
        **{'Pin bold (vastag)': 'Azores Whale Watching', 'Pin light (vekony)': "what no one tells you before you go"},
        URL='https://milesandflavors.com/azores-whale-watching/',
        Board='Best Things to Do Around the World',
        **{'Pin cim': 'Azores Whale Watching: The Complete Guide (What to Expect + Best Tours)',
           'Pin leiras': "Sperm whales don't just pass through the Azores on migration — they live here year-round, in some of the deepest water in the Atlantic. That's why the success rate is so different from anywhere else in Europe. This isn't a 'maybe you'll see a fin' experience. Complete guide: best season, how to book, what species to expect, and the honest truth about seasickness and bad weather days.",
           'Alt text': 'A sperm whale surfacing and diving in the deep blue waters off São Miguel island, Azores, with a small whale watching boat visible in the distance.'}
    ),
    dict(
        Cikk='Azores Whale Watching',
        **{'Pin #': '2'},
        Template='Title bottom dark',
        Photos='1',
        **{'Pin bold (vastag)': 'Sperm Whales in the Azores', 'Pin light (vekony)': 'the bucket list experience worth every euro'},
        URL='https://milesandflavors.com/azores-whale-watching/',
        Board='Bucket list destinations',
        **{'Pin cim': 'Whale Watching in the Azores: Is It Worth It? (Honest Review)',
           'Pin leiras': "Most whale watching is: cold boat, distant splash, technically a whale. Azores whale watching is something else entirely. Resident sperm whales, former whalers-turned-guides who know every dive pattern, and the deepest part of the Atlantic right outside the harbour. Honest review of what it's actually like, which operators are genuinely good, and whether the price is worth it. (It is.)",
           'Alt text': 'A humpback whale breaching the surface of the Atlantic Ocean near the Azores islands, with blue sky and ocean spray.'}
    ),
    dict(
        Cikk='Azores Whale Watching',
        **{'Pin #': '3'},
        Template='Centered dark',
        Photos='1',
        **{'Pin bold (vastag)': 'Best Whale Watching in Europe?', 'Pin light (vekony)': "the Azores aren't even a debate"},
        URL='https://milesandflavors.com/azores-whale-watching/',
        Board='Best Things to Do Around the World',
        **{'Pin cim': 'Azores Whale Watching Guide: Best Tours, Season & What to Expect',
           'Pin leiras': "The lookout spotters stand on the cliffs above São Miguel with binoculars, radio the boats when a whale surfaces, and guide them in. It's a system built by people who used to hunt these animals and now dedicate their lives to protecting them. Azores whale watching is special in ways that go far beyond sighting rates. Best operators, how to book, and what to expect every month of the year.",
           'Alt text': 'A whale watching guide pointing toward a surfacing sperm whale near a small eco-tour boat off the coast of São Miguel, Azores.'}
    ),
    dict(
        Cikk='Azores Whale Watching',
        **{'Pin #': '4'},
        Template='Title top dark',
        Photos='1',
        **{'Pin bold (vastag)': 'São Miguel Whale Watching', 'Pin light (vekony)': 'book this before anything else'},
        URL='https://milesandflavors.com/azores-whale-watching/',
        Board='Europe Travel Itineraries',
        **{'Pin cim': 'São Miguel Whale Watching: How to Book, What to Know & Best Season',
           'Pin leiras': "Book this before anything else on your São Miguel itinerary — not because it's the most convenient, but because the best tours fill up fast and weather windows close. Sperm whales year-round, humpbacks and blue whales in season, a stretch of Atlantic so deep it feels like the edge of the world. Practical guide: when to book, which operators have the best track record, what to do if conditions force a cancel.",
           'Alt text': 'Close-up of a sperm whale tail fluke raised above the ocean surface as it dives deep off the coast of the Azores islands.'}
    ),

    # ── Montserrat Day Trip from Barcelona (5 pin) ──
    dict(
        Cikk='Montserrat Day Trip from Barcelona',
        **{'Pin #': '1'},
        Template='Title top light',
        Photos='1',
        **{'Pin bold (vastag)': 'Montserrat Day Trip', 'Pin light (vekony)': 'from Barcelona, worth every minute'},
        URL='https://milesandflavors.com/montserrat-day-trip-from-barcelona/',
        Board='Spain Travel Guide',
        **{'Pin cim': 'Montserrat Day Trip from Barcelona: The Complete Honest Guide',
           'Pin leiras': "The rock formations at Montserrat look like they were carved by something that didn't care about the rules — vertical, serrated, reddish, impossible. And clinging to the face of them: a monastery that has been there since the 9th century. Complete Montserrat day trip guide from Barcelona: how to get there (rack railway vs cable car, honestly compared), what to do with a full day, and how to avoid the crowds.",
           'Alt text': 'The jagged serrated rock formations of Montserrat mountain towering above the monastery, viewed from the Sant Joan hiking trail above Barcelona.'}
    ),
    dict(
        Cikk='Montserrat Day Trip from Barcelona',
        **{'Pin #': '2'},
        Template='Title bottom dark',
        Photos='1',
        **{'Pin bold (vastag)': 'Cable Car or Rack Railway?', 'Pin light (vekony)': 'the Montserrat question everyone Googles'},
        URL='https://milesandflavors.com/montserrat-day-trip-from-barcelona/',
        Board='Day Trips & Excursions',
        **{'Pin cim': 'Montserrat Cable Car vs Rack Railway: Which One Should You Take?',
           'Pin leiras': "Everyone Googles 'Montserrat cable car or rack railway' before they go — and most articles still don't actually help you decide. The answer depends on what kind of traveller you are and what time you're going. Real breakdown: what the experience is like on each, the difference in views, how long each takes, and which one I'd choose (and exactly why).",
           'Alt text': 'The Montserrat cable car ascending the dramatic rocky cliffs with the monastery visible far below against the Barcelona plain stretching to the horizon.'}
    ),
    dict(
        Cikk='Montserrat Day Trip from Barcelona',
        **{'Pin #': '3'},
        Template='Centered light',
        Photos='1',
        **{'Pin bold (vastag)': 'Montserrat, Spain', 'Pin light (vekony)': 'the day trip that steals the show'},
        URL='https://milesandflavors.com/montserrat-day-trip-from-barcelona/',
        Board='Spain Travel Guide',
        **{'Pin cim': 'Montserrat from Barcelona: What to Do, See & Eat (Full Day Guide)',
           'Pin leiras': "Most people see the monastery and leave by 1pm. The hikers who stay until late afternoon see something else entirely — the mountain without the crowds, trails that rise above the cloud line, a silence you didn't expect this close to Barcelona. How to spend a full day at Montserrat: the hikes worth doing, where to eat, and why leaving early is the main mistake visitors make.",
           'Alt text': 'Hikers on the rocky Sant Joan trail above Montserrat with the monastery and the Catalan countryside stretching far below.'}
    ),
    dict(
        Cikk='Montserrat Day Trip from Barcelona',
        **{'Pin #': '4'},
        Template='Title bottom light',
        Photos='1',
        **{'Pin bold (vastag)': 'Barcelona → Montserrat', 'Pin light (vekony)': "the day trip you'll talk about for years"},
        URL='https://milesandflavors.com/montserrat-day-trip-from-barcelona/',
        Board='Bucket list destinations',
        **{'Pin cim': "Montserrat Day Trip: Is It Worth It? (Honest Take + What to Skip)",
           'Pin leiras': "The people who come home underwhelmed from Montserrat all did the same thing: monastery, photo, back to Barcelona. The people who can't stop talking about it did something different — they stayed, they hiked, they watched the morning mist burn off the peaks. Same mountain, completely different day. Honest guide to getting the version that actually stays with you.",
           'Alt text': 'Morning mist clearing over the dramatic rocky pinnacles of Montserrat mountain in Catalonia, Spain, with pale golden light hitting the peaks.'}
    ),
    dict(
        Cikk='Montserrat Day Trip from Barcelona',
        **{'Pin #': '5'},
        Template='Accent',
        Photos='1',
        **{'Pin bold (vastag)': 'Day Trips from Barcelona', 'Pin light (vekony)': 'Montserrat is not optional'},
        URL='https://milesandflavors.com/montserrat-day-trip-from-barcelona/',
        Board='Spain Travel Guide',
        **{'Pin cim': 'Best Day Trips from Barcelona: Why Montserrat Should Be First on Your List',
           'Pin leiras': "If you're in Barcelona for a week and only have time for one day trip — make it Montserrat. Not because it's the most popular, but because it's the one that actually stays with you. Ancient monastery on the edge of impossible rock formations, trails above the clouds, views that stretch to the Pyrenees on a clear morning. Everything you need to plan it properly from Barcelona.",
           'Alt text': 'Wide panoramic view of Montserrat mountain at sunrise with pink and golden light illuminating the serrated rocky peaks in Catalonia.'}
    ),

    # ── Chicago Architecture River Cruise (5 pin) ──
    dict(
        Cikk='Chicago Architecture River Cruise',
        **{'Pin #': '1'},
        Template='Title top light',
        Photos='1',
        **{'Pin bold (vastag)': 'Chicago Architecture Cruise', 'Pin light (vekony)': 'the one thing every Chicago visitor does'},
        URL='https://milesandflavors.com/chicago-architecture-river-cruise/',
        Board='Chicago Travel Guide',
        **{'Pin cim': 'Chicago Architecture River Cruise: Everything You Need to Know',
           'Pin leiras': "The Chicago river cruise is one of the only tourist activities where locals will look you in the eye and say 'yes, actually do that one.' Two hours on the river, looking up at skyscrapers you finally understand — because someone is telling you the story behind each one. Complete guide: which tour to book, the best time of day to go, and what changes when you see Chicago from the water.",
           'Alt text': 'The Chicago skyline reflected in the calm Chicago River at golden hour with skyscrapers towering on both sides during an architecture boat tour.'}
    ),
    dict(
        Cikk='Chicago Architecture River Cruise',
        **{'Pin #': '2'},
        Template='Title bottom dark',
        Photos='1',
        **{'Pin bold (vastag)': 'Chicago River Cruise', 'Pin light (vekony)': 'worth it or tourist trap?'},
        URL='https://milesandflavors.com/chicago-architecture-river-cruise/',
        Board='USA Travel Itineraries',
        **{'Pin cim': 'Chicago Architecture Boat Tour: Is It Actually Worth It? (Honest Review)',
           'Pin leiras': "Every Chicago guide recommends the architecture river cruise. That either makes you want to book it immediately — or makes you suspicious it's overhyped. It's neither. It's one of those rare activities that over-delivers precisely because the bar is already high. Honest review: what the two hours are actually like, what you learn that you couldn't get from the Riverwalk, and whether the price holds up.",
           'Alt text': 'A Chicago architecture river cruise boat passing beneath a historic drawbridge with glass skyscrapers rising above on both sides of the river.'}
    ),
    dict(
        Cikk='Chicago Architecture River Cruise',
        **{'Pin #': '3'},
        Template='Centered light',
        Photos='1',
        **{'Pin bold (vastag)': 'Chicago Skyline', 'Pin light (vekony)': 'seen best from the river'},
        URL='https://milesandflavors.com/chicago-architecture-river-cruise/',
        Board='Chicago Travel Guide',
        **{'Pin cim': 'Chicago Architecture Cruise: Best Time to Go, How to Book & What to See',
           'Pin leiras': "From the sidewalk, Chicago's skyscrapers are impressive. From the river, they make sense — you see the whole building, the relationship between them, each era of architecture answering the one before it. The river cruise is the best 90-minute architecture education you'll ever get. Best time of day (not noon), which operators actually know their buildings, and what you'll see on the water.",
           'Alt text': 'View from the water of Chicago dramatic mixed-era skyline including the Willis Tower and Marina City corncob towers during an afternoon architecture cruise.'}
    ),
    dict(
        Cikk='Chicago Architecture River Cruise',
        **{'Pin #': '4'},
        Template='Title top dark',
        Photos='1',
        **{'Pin bold (vastag)': 'Best Things to Do in Chicago', 'Pin light (vekony)': 'the Architecture Cruise is #1 for a reason'},
        URL='https://milesandflavors.com/chicago-architecture-river-cruise/',
        Board='Chicago Travel Guide',
        **{'Pin cim': 'Chicago Architecture River Cruise: How to Book the Best Tour',
           'Pin leiras': "Put the architecture river cruise on day one of your Chicago trip. Not because it's the flashiest thing you'll do — because it reframes everything else. After two hours on the river you'll walk through the Loop differently. You'll know what you're looking at. You'll understand why this city invented skyscrapers. How to book, when to go, and why the time slot matters more than most people realise.",
           'Alt text': 'The Chicago River from water level looking toward the glittering city skyline, flanked by historic and modern skyscrapers in the late afternoon light.'}
    ),
    dict(
        Cikk='Chicago Architecture River Cruise',
        **{'Pin #': '5'},
        Template='Title bottom light',
        Photos='1',
        **{'Pin bold (vastag)': 'Chicago Architecture', 'Pin light (vekony)': 'the river cruise locals actually recommend'},
        URL='https://milesandflavors.com/chicago-architecture-river-cruise/',
        Board='USA Travel Itineraries',
        **{'Pin cim': "Chicago Architecture River Cruise: Tips, Operators & Why It's Worth Every Dollar",
           'Pin leiras': "Not all Chicago river cruises are the same. Some are excellent. Some are expensive, rushed, and led by guides who clearly learned from a script. The difference comes down to two things: operator and time slot. Which companies consistently get five stars from people who actually know architecture, why 12pm is the worst slot, and how to make sure you get the version that's worth every dollar.",
           'Alt text': 'Close-up of the ornate facades of Chicago historic skyscrapers towering over the Chicago River, viewed from a passing architecture tour boat.'}
    ),
]

# ── Ütemezés: forgórendszer, ugyanaz az URL legalább 5 naponta ───────────────
# Sorrend a NEW_PINS listával megegyező (São Miguel 1-5, BestTime 1-3, Whale 1-4, Mont 1-5, Chi 1-5)
# Forgókör: São Miguel (SM), Best Time Azores (BT), Whale Watching (WW), Montserrat (MT), Chicago (CH)
#   Kör 1: Jun 20 SM, Jun 21 BT, Jun 22 WW, Jun 23 MT, Jun 24 CH
#   Kör 2: Jun 25 SM, Jun 26 BT, Jun 27 WW, Jun 28 MT, Jun 29 CH
#   Kör 3: Jun 30 SM, Jul  1 BT, Jul  2 WW, Jul  3 MT, Jul  4 CH
#   Kör 4: Jul  5 SM, (BT kész), Jul  7 WW, Jul  8 MT, Jul  9 CH
#   Kör 5: Jul 10 SM, (BT kész), (WW kész), Jul 13 MT, Jul 14 CH
# Minden cikken belül egymást követő pinek között >= 5 nap.
TARGET_DATES = [
    # São Miguel pin1–5 (5 naponként)
    '2026.06.20',
    '2026.06.25',
    '2026.06.30',
    '2026.07.05',
    '2026.07.10',
    # Best Time to Visit Azores pin1–3 (5 naponként)
    '2026.06.21',
    '2026.06.26',
    '2026.07.01',
    # Azores Whale Watching pin1–4 (5 naponként)
    '2026.06.22',
    '2026.06.27',
    '2026.07.02',
    '2026.07.07',
    # Montserrat pin1–5 (5 naponként)
    '2026.06.23',
    '2026.06.28',
    '2026.07.03',
    '2026.07.08',
    '2026.07.13',
    # Chicago Architecture pin1–5 (5 naponként)
    '2026.06.24',
    '2026.06.29',
    '2026.07.04',
    '2026.07.09',
    '2026.07.14',
]

DAILY_SLOTS = ['20:00', '21:00', '22:00', '23:00', '0:00', '1:00', '2:00']
DISPLACEMENT_SLOT = '20:00'  # ezt a slotot "vesszük el" minden célnapon

# ── Fő logika ────────────────────────────────────────────────────────────────

def load_csv():
    rows = []
    with open(CSV_PATH, encoding='utf-8-sig') as f:
        reader = csv.DictReader(f, delimiter=';')
        fieldnames = reader.fieldnames
        for row in reader:
            rows.append(row)
    return rows, fieldnames

def find_displaced(rows, target_dates, slot):
    """A célnapokon SLOT-ban lévő sorok indexeit adja vissza."""
    displaced = []
    for i, row in enumerate(rows):
        if row['Datum'] in target_dates and row['Idopont'] == slot:
            displaced.append(i)
    return displaced

def next_extension_slots(rows):
    """Júl. 17 után következő szabad (dátum, időpont) párok generátora."""
    existing = set((r['Datum'], r['Idopont']) for r in rows)
    d = datetime(2026, 7, 18)
    slot_idx = 0
    while True:
        ds = d.strftime('%Y.%m.%d')
        ts = DAILY_SLOTS[slot_idx]
        if (ds, ts) not in existing:
            yield ds, ts
        slot_idx += 1
        if slot_idx >= len(DAILY_SLOTS):
            slot_idx = 0
            d += timedelta(days=1)

def validate_5day_rule(pins, dates):
    """Ellenőrzi, hogy azonos URL-en belül minden pin >= 5 napra van egymástól."""
    from collections import defaultdict
    url_dates = defaultdict(list)
    for pin, date in zip(pins, dates):
        url_dates[pin['URL']].append(date)
    errors = []
    for url, ds in url_dates.items():
        ds_sorted = sorted(ds)
        for i in range(1, len(ds_sorted)):
            d1 = datetime.strptime(ds_sorted[i-1], '%Y.%m.%d')
            d2 = datetime.strptime(ds_sorted[i], '%Y.%m.%d')
            gap = (d2 - d1).days
            if gap < 5:
                errors.append(f"  {url.split('/')[-2]}: {ds_sorted[i-1]} -> {ds_sorted[i]} = {gap} nap (minimum 5)")
    return errors

def run(mode='preview'):
    rows, fieldnames = load_csv()

    # 0. 5-napos szabály ellenőrzése
    errors = validate_5day_rule(NEW_PINS, TARGET_DATES)
    if errors:
        print("HIBA: 5 napos linkelési szabály SÉRÜL:")
        for e in errors: print(e)
        sys.exit(1)

    # 1. Megkeressük a 22 kiszorítandó sort
    displaced_indices = find_displaced(rows, TARGET_DATES, DISPLACEMENT_SLOT)

    if len(displaced_indices) != len(TARGET_DATES):
        print(f"FIGYELEM: {len(TARGET_DATES)} celnapot kertunk, de csak "
              f"{len(displaced_indices)} sort talaltunk a {DISPLACEMENT_SLOT} slotban.")
        missing = set(TARGET_DATES) - set(rows[i]['Datum'] for i in displaced_indices)
        if missing:
            print(f"   Hianyzó datumok: {sorted(missing)}")

    # 2. Kiszorított sorok -> jul. 18+ slotokba
    ext_gen = next_extension_slots(rows)
    displaced_moves = []
    for idx in displaced_indices:
        new_date, new_time = next(ext_gen)
        displaced_moves.append((idx, new_date, new_time))

    # 3. Összepárosítjuk az új pineket a célnapokkal
    assert len(NEW_PINS) == len(TARGET_DATES), \
        f"Pin count ({len(NEW_PINS)}) != celnapok ({len(TARGET_DATES)})"

    print("=" * 70)
    print(f"PREVIEW -- {len(displaced_moves)} sor KITOLVA jul. 18 utanra:")
    print("=" * 70)
    for idx, new_date, new_time in displaced_moves:
        r = rows[idx]
        print(f"  {r['Datum']} {r['Idopont']}  {r['Cikk']} pin{r['Pin #']}"
              f"  ->  {new_date} {new_time}")

    print()
    print("=" * 70)
    print(f"22 UJ PIN beillesztve:")
    print("=" * 70)
    for i, (pin, date) in enumerate(zip(NEW_PINS, TARGET_DATES)):
        print(f"  {date} {DISPLACEMENT_SLOT}  {pin['Cikk']} pin{pin['Pin #']}"
              f"  [{pin['Board'][:35]}]")

    if mode == 'preview':
        print()
        print("Futtasd: python inject_new_articles.py write")
        return

    # ── WRITE mód ──
    # Backup
    shutil.copy(CSV_PATH, BACKUP_PATH)
    print(f"\nBackup mentve: {BACKUP_PATH}")

    # Módosítjuk a kiszorított sorokat
    for idx, new_date, new_time in displaced_moves:
        rows[idx]['Datum'] = new_date
        rows[idx]['Idopont'] = new_time

    # Új sorokat szúrunk be (a célnap + DISPLACEMENT_SLOT-ba)
    for pin, date in zip(NEW_PINS, TARGET_DATES):
        new_row = {k: '' for k in fieldnames}
        new_row['Datum'] = date
        new_row['Idopont'] = DISPLACEMENT_SLOT
        for k, v in pin.items():
            if k in new_row:
                new_row[k] = v
        rows.append(new_row)

    # Rendezzük dátum + idő szerint
    def sort_key(r):
        d = r.get('Datum', '') or '9999.99.99'
        t = r.get('Idopont', '') or '99:99'
        return (d, t)

    rows.sort(key=sort_key)

    # Kiírjuk
    with open(CSV_PATH, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        writer.writerows(rows)

    print(f"pins.csv frissitve. Osszesen: {len(rows)} sor.")
    print(f"   Regi sorok: {len(rows) - len(NEW_PINS)}")
    print(f"   Uj pinek: {len(NEW_PINS)}")


if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'preview'
    run(mode)

