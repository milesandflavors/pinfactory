"""
Pin leírás frissítő — érzelmes + természetesen kulcsszavas stílus
Futtatás: python update_descriptions.py
"""
import csv, os, shutil
from datetime import datetime

CSV_PATH = r"D:\Travel blog\PinFactory\pins.csv"
BACKUP   = CSV_PATH.replace(".csv", f"_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.csv")

# Frissített leírások: {(Cikk, Pin #): új leírás}
NEW_DESCRIPTIONS = {

# ── 12-Day Greece Itinerary ──────────────────────────────────────────────────
("12-Day Greece Itinerary", "5"): "Santorini for the caldera views. Naxos for the beaches locals actually swim at. Milos for the sea caves. Athens for the Acropolis at dawn when you're nearly alone inside it. A 12-day Greece island-hopping itinerary with the ferry schedule, best villages to base yourself in, and exactly how many nights each island deserves.",
("12-Day Greece Itinerary", "6"): "The Acropolis is worth it. The Santorini caldera is worth it. But the best Greece moments come from the quieter Cyclades — Milos, Folegandros, Sifnos — that most 12-day Greece itineraries skip entirely. A first-timer's route that balances the bucket list with the hidden islands.",
("12-Day Greece Itinerary", "7"): "A caldera sunset in Santorini is the kind of thing that makes you want to cancel your flight home. This 12-day Greece itinerary is built around the moments worth staying for — Athens sightseeing, Greek island hopping, Santorini sunsets — with the complete ferry schedule and booking guide.",
("12-Day Greece Itinerary", "8"): "Which ferry, which order, how many nights on each island — the logistics questions that derail every first Greece trip, answered clearly. A 12-day Greece island-hopping itinerary for first-timers: Athens, Santorini, Mykonos, and Naxos, with exact connections and what to book in advance.",
("12-Day Greece Itinerary", "9"): "Ruins older than your imagination, beaches that make you stop mid-sentence, islands that look painted. This 12-day Greece itinerary covers Athens sightseeing, Santorini's caldera villages, and the best of the Cyclades — a complete first-timer's Greece travel guide, day by day.",

# ── Amalfi Coast 5-Day Itinerary ─────────────────────────────────────────────
("Amalfi Coast 5-Day Itinerary", "5"): "The Path of the Gods puts the whole Amalfi Coast below you — sea glittering 500 meters down, Positano visible in the distance, no crowds until mid-morning. Where this iconic coastal hike fits into a 5-day Amalfi Coast itinerary, with the ferry routes, best base towns, and what to book ahead.",
("Amalfi Coast 5-Day Itinerary", "6"): "Where to base yourself, how the ferries actually work between Positano, Amalfi, and Ravello, which towns are worth the night and which to visit by day boat. Everything to know before you book the Amalfi Coast — a complete Southern Italy travel guide so nothing surprises you when you arrive.",
("Amalfi Coast 5-Day Itinerary", "7"): "Cliffside villages glowing at golden hour, water so turquoise it looks painted, lemon terraces scenting the air above the sea. The most beautiful places on the Amalfi Coast — Positano, Ravello, Atrani, the hidden coves — and a 5-day itinerary built around all of them.",

# ── 4 Days in Barcelona ───────────────────────────────────────────────────────
("4 Days in Barcelona", "5"): "Four days in Barcelona that cover everything worth doing: Sagrada Familia at morning light when the stained glass is extraordinary, tapas afternoons in El Born, beach time, and the Bunkers del Carmel at sunset with the whole city below. The perfect first-timer Barcelona itinerary.",
("4 Days in Barcelona", "6"): "No backtracking, no wasted hours crossing the city. A 4-day Barcelona itinerary grouped by area — Gaudí mornings in the Eixample, Gothic Quarter afternoons, Barceloneta beach, and Park Güell before the crowds. Spain travel guide for first-timers who want to see it all without the rush.",
("4 Days in Barcelona", "7"): "The Bunkers del Carmel at golden hour: the whole Barcelona skyline stretching to the Mediterranean, everyone watching the sun drop together, no entrance fee. The moment that closes every great Barcelona trip. Plus Sagrada Família, El Born, and everything else your 4 days should include.",

# ── Barcelona Bucket List ─────────────────────────────────────────────────────
("Barcelona Bucket List", "4"): "Las Ramblas will disappoint you. The Bunkers del Carmel won't. The hidden side of the Barcelona bucket list: Gràcia's village squares, El Born's cocktail bars, Montjuïc at dusk, and the lesser-known spots that make you want to move here. Barcelona travel guide beyond the tourist trail.",
("Barcelona Bucket List", "5"): "Some Barcelona bucket-list items are worth every minute of the queue. Some aren't. An honest ranking of everything famous to do in Barcelona — from Sagrada Família and Park Güell to Barceloneta beach and the Gothic Quarter — so you spend your days on the ones that actually earn it.",
("Barcelona Bucket List", "6"): "We came for Gaudí and left obsessed with the whole city: the tapas dinners that start at 10pm, the Bunkers del Carmel sunsets, the Gothic Quarter lanes. Barcelona's complete bucket list — Sagrada Família, Park Güell, El Born, Barceloneta — and what to do in the right order.",
("Barcelona Bucket List", "7"): "Short on time in Barcelona? The essential list is short: Sagrada Família at morning light, Gothic Quarter wandering, the Bunkers del Carmel at sunset, and one long tapas dinner in El Born. The Barcelona highlights that earn every minute — a first-timer's Spain travel guide.",

# ── Where to Stay in NYC (NEW) ────────────────────────────────────────────────
("Where to Stay in NYC (NEW)", "1"): "Midtown is convenient and soulless after dark. The West Village is beautiful and expensive. Brooklyn is great value if you're fine with one subway stop to Manhattan. The best New York neighborhoods compared — Midtown, Chelsea, the Village, Upper West Side, and Brooklyn — so you book the right NYC hotel location.",
("Where to Stay in NYC (NEW)", "2"): "Before you book New York, read this: Midtown for access, the West Village or SoHo for atmosphere, Brooklyn for value and local feel. The Manhattan vs Brooklyn decision explained clearly — a neighborhood guide for first-time New York visitors.",
("Where to Stay in NYC (NEW)", "3"): "Central Manhattan convenience or Brooklyn character and lower prices? How to choose your New York base — Midtown, Chelsea, Lower East Side, Williamsburg — what each neighborhood is really like and what kind of NYC trip each one suits.",
("Where to Stay in NYC (NEW)", "4"): "Smart New York neighborhoods close to the subway and the main sights without Midtown hotel pricing. Where to stay in NYC for first-timers who want value and location: the Lower East Side, Astoria, Long Island City, and the best budget-friendly Manhattan alternatives.",

# ── Montserrat Day Trip from Barcelona ───────────────────────────────────────
("Montserrat Day Trip from Barcelona", "1"): "Montserrat is one of those places that genuinely earns its hype — reddish serrated rock formations rising 1,200 meters above Barcelona, a Benedictine monastery that's been here since the 9th century, and hiking trails that put all of Catalonia below your feet. Everything to know before your Barcelona day trip.",
("Montserrat Day Trip from Barcelona", "2"): "Cable car or rack railway to Montserrat? Here's the honest answer — and everything else to know before you go, from what to skip to when to arrive for the best views. The complete Montserrat day trip guide from Barcelona, with timings and ticket advice.",
("Montserrat Day Trip from Barcelona", "3"): "Most Montserrat day-trippers come for the monastery and leave before lunch. The hikers who stay longer find empty trails, peaks above the cloud line, and a version of Montserrat that feels like an entirely different place. A day trip from Barcelona worth making the most of.",
("Montserrat Day Trip from Barcelona", "4"): "Worth it? Absolutely. But the cable car vs. train decision, the morning vs. afternoon timing, and which trails to take — these choices determine whether your Montserrat day trip from Barcelona is magical or mediocre. The practical guide that gets the details right.",
("Montserrat Day Trip from Barcelona", "5"): "There are good day trips from Barcelona, and then there's Montserrat — in a category of its own. Serrated rock spires, a Benedictine monastery, Catalan mountain hiking trails above the clouds, and views that stretch to the sea on clear days. The one day trip from Barcelona that's genuinely unmissable.",

# ── Amsterdam Bucket List ─────────────────────────────────────────────────────
("Amsterdam Bucket List", "4"): "A canal cruise at golden hour. The Van Gogh Museum with a timed ticket before the tour groups. A bike ride through Vondelpark and the Jordaan's quiet backstreets. The Amsterdam must-dos that actually live up to the hype — a first-timer's Netherlands travel guide with the honest picks.",

# ── Best Things to Do in Tokyo ────────────────────────────────────────────────
("Best Things to Do in Tokyo", "4"): "Ramen that costs 7 euros and takes an hour to make. Sushi at 7am in Tsukiji outer market. Convenience store snacks that beat any packaged food you've tasted. Eating your way through Tokyo — the best food experiences in Japan's capital, from Shibuya izakayas to Shinjuku ramen alleys.",

# ── Amalfi Coast Bucket List ──────────────────────────────────────────────────
("Amalfi Coast Bucket List", "4"): "Fornillo Beach instead of Positano's main strip. Furore's hidden fjord. The coves only accessible by kayak. The Amalfi Coast swims that require a little effort — and reward you with the kind of afternoon you talk about for years. Southern Italy travel guide for the beaches worth finding.",
("Amalfi Coast Bucket List", "5"): "An honest take on the Amalfi hype: which experiences earn the trip (a boat day to hidden coves, Ravello at sunset, the Path of the Gods hike) and which to skip. The Amalfi Coast bucket list that the coast actually delivers on — Italy travel tips for first-timers.",
("Amalfi Coast Bucket List", "6"): "Positano lit gold at 8pm. Ravello above the last cloud, garden terraces overlooking the Tyrrhenian Sea. The Amalfi Coast sunsets worth planning an entire evening around — where to be, what to book, and which terrace gets the light right. Southern Italy travel guide.",
("Amalfi Coast Bucket List", "7"): "The clifftop path that runs above the sea. The Amalfi villages unchanged for a hundred years. The meals on terraces with nothing but Mediterranean water in front of you. The Amalfi Coast experiences worth building an Italy vacation around — bucket list for first-timers and return visitors alike.",

# ── Where to Stay in Rome (NEW) ───────────────────────────────────────────────
("Where to Stay in Rome (NEW)", "1"): "Monti has the best trattorias and the most local character. Centro Storico gives you the icons on foot. Trastevere has the evening atmosphere. The best Rome neighborhoods for first-time visitors compared — Monti, Trastevere, Centro Storico, Prati — so you book the right Rome hotel location.",
("Where to Stay in Rome (NEW)", "2"): "Cobbled lanes, dinner spots that fill up by 8pm, and the Colosseum a 10-minute walk away — why Monti and Trastevere are the best Rome neighborhoods for a first trip. Italy travel guide for first-timers choosing between Rome's most charming areas.",
("Where to Stay in Rome (NEW)", "3"): "Before you book Rome, read this: Monti for charm and value, Centro Storico for being in the middle of everything, Trastevere for evening atmosphere and cobbled piazzas. The Rome neighborhood guide that makes the hotel decision simple — first-timer's Italy travel tips.",
("Where to Stay in Rome (NEW)", "4"): "The Rome neighborhoods that keep you walking distance from the Colosseum, the Pantheon, and Trastevere — without paying Vatican-view hotel prices. Where to stay in Rome for the best combination of value, location, and authentic Italian neighborhood atmosphere.",

# ── Hakone Day Trip from Tokyo ────────────────────────────────────────────────
("Hakone Day Trip from Tokyo", "1"): "Mt Fuji on a clear morning from the Hakone ropeway, Lake Ashi glittering below. An onsen soak in the afternoon. Back in Tokyo for dinner. The complete Hakone day trip guide from Tokyo — what to see, how to use the Hakone Free Pass, and how to make the day flow without wasting an hour.",
("Hakone Day Trip from Tokyo", "2"): "The easiest way to see Mt Fuji from Tokyo: a Hakone day trip with the ropeway over volcanic valleys, Lake Ashi by boat, and enough time for a traditional onsen soak. Everything you need to plan it, including the Hakone Free Pass, best departure times, and what to do if Fuji is cloudy.",
("Hakone Day Trip from Tokyo", "3"): "Mt Fuji is often hidden in clouds. The ropeway runs regardless. The onsen exists in any weather. Hakone is worth the day trip from Tokyo even without the mountain views — and extraordinary when you get them. An honest Japan travel guide for planning the perfect Hakone day.",
("Hakone Day Trip from Tokyo", "4"): "Train, ropeway, lake boat, bus — the Hakone loop sounds complicated and isn't once you understand it. How to see Mt Fuji, Lake Ashi, and the Owakudani volcanic valley in one smooth day trip from Tokyo, with the Hakone Free Pass explained and the route mapped out.",

# ── Where to Stay on the Amalfi Coast ────────────────────────────────────────
("Where to Stay on the Amalfi Coast", "3"): "Towns that keep you ferry-connected without Positano prices: Praiano for clifftop quiet, Atrani for a local village feel, Cetara for the best food on the coast. The smart Amalfi Coast bases that give you everything without the famous-town premium — Southern Italy travel guide.",
("Where to Stay on the Amalfi Coast", "4"): "Waking to the coast from your terrace, the Tyrrhenian Sea below, no sound except the waves and the distant ferry horn. The Amalfi Coast hotels and guesthouses where the view is the whole experience — and how to find them before they book out.",
("Where to Stay on the Amalfi Coast", "5"): "Ferry-linked, walkable Amalfi towns where you don't need to navigate the cliff road every day — Positano, Praiano, Amalfi, Minori. The most livable Amalfi Coast bases for a week on the Italian coast without a car, with honest hotel area recommendations.",
("Where to Stay on the Amalfi Coast", "6"): "Positano has the crowds and the beauty in equal measure. Praiano has the quiet and the same sunsets for half the price. Ravello has the gardens above the sea. The Amalfi towns that stay calm when the main strip is packed — and why they're the smarter choice.",
("Where to Stay on the Amalfi Coast", "7"): "Before you book the Amalfi Coast, read this: Positano is beautiful and crowded, Praiano is the smart local alternative, and Ravello is for people who want Italian garden views over beach time. The honest Amalfi hotel location guide — where each type of traveler should actually stay.",

# ── Chicago Architecture River Cruise ────────────────────────────────────────
("Chicago Architecture River Cruise", "1"): "The Chicago Architecture Foundation river cruise is one of those rare tourist activities that's genuinely worth more than it costs. You're floating through a canyon of skyscrapers while an expert explains exactly what you're looking at. Everything to know before you book — which tour to choose, when to go, and why it tops every Chicago itinerary.",
("Chicago Architecture River Cruise", "2"): "The Chicago Architecture River Cruise gets recommended in every travel guide ever written about the city — and for once, the recommendation is right. What the experience is actually like, which cruise to book among the options, and what separates a great docent-led tour from a mediocre recorded-audio one.",
("Chicago Architecture River Cruise", "3"): "The Chicago skyline looks completely different from the river. Better, actually — you see the full scale of the buildings, the stories behind them, and the waterway that made the whole city possible. Why the architecture river cruise belongs at the very top of any Chicago itinerary.",
("Chicago Architecture River Cruise", "4"): "If you're building a Chicago itinerary, the architecture river cruise belongs at the top. It's the best 90-minute introduction to the city you can get — and it makes every skyscraper you see afterward mean something. How to book, which tour operator to pick, and the best time of day to go.",
("Chicago Architecture River Cruise", "5"): "Not all Chicago architecture cruises are equal. Some have expert docents who permanently change how you see the skyline. Some have recorded audio and weak cocktails. Here's how to tell the difference and book the right one — Chicago travel tips for first-timers.",

# ── Best Day Trips from Amsterdam ─────────────────────────────────────────────
("Best Day Trips from Amsterdam", "4"): "A car-free village where everyone travels by boat. Giethoorn is 90 minutes from Amsterdam and looks like it belongs in a fairy tale. The most beautiful Amsterdam day trip for first-timers — and the other Netherlands day trips worth the journey: Keukenhof tulip fields, Zaanse Schans windmills, Haarlem.",

# ── Best Beaches in Zakynthos ─────────────────────────────────────────────────
("Best Beaches in Zakynthos", "4"): "Some of Zakynthos's best beaches are reachable by car, no boat required. Gerakas sea turtle beach, Porto Limnionas' rocky cove, and the west coast swims you can drive to in a morning. The complete guide to Zakynthos beaches for first-timers — what to expect, when to go, and which are worth the detour.",
("Best Beaches in Zakynthos", "5"): "Navagio Shipwreck Beach is only accessible by boat — the sheer limestone cliffs, the rusting wreck, the water so blue it looks filtered. The Blue Caves glow turquoise from beneath the boat. And they are worth every minute of the trip. What to expect, which boat tour to take, and when to arrive for the best light.",
("Best Beaches in Zakynthos", "6"): "Loggerhead sea turtles surfacing at Gerakas at dawn. The Blue Caves lit from below in impossible turquoise. Navagio's shipwreck half-buried in white sand. The Zakynthos beaches that feel like wildlife encounters and the ones that feel like living inside a painting — Greece travel guide.",
("Best Beaches in Zakynthos", "7"): "Family-friendly coves with shallow snorkeling water, dramatic cliffs with no crowds, hidden inlets you nearly swim past before noticing them. The best beaches in Zakynthos sorted by what you actually want from a Greek island beach day — a Greece travel guide for every type of beach lover.",
("Best Beaches in Zakynthos", "8"): "Navagio's shipwreck, the Blue Caves, Porto Limnionas, Gerakas — the Zakynthos beaches worth rearranging your whole Greece trip around. What to book, when to go, which are best for snorkeling vs. swimming, and how to see them all without spending two days on boat queues.",

# ── Best Things to Do in Rome (NEW) ──────────────────────────────────────────
("Best Things to Do in Rome (NEW)", "4"): "The Colosseum at opening time, before the tour groups arrive. The Trevi Fountain after 10pm, quiet and glowing with no one between you and 18th-century stone. The Aventine keyhole with St Peter's dome perfectly framed. The Rome experiences worth timing right — Italy travel tips for a first-time visit.",
("Best Things to Do in Rome (NEW)", "5"): "The Colosseum, the Vatican, the Pantheon, Trastevere — the Rome must-dos that make a first trip work, timed correctly and booked smart. What to see, what to book in advance, and what to save for a last-minute dinner decision. The complete first-timer Rome travel guide.",
("Best Things to Do in Rome (NEW)", "6"): "The Pantheon's open dome letting in afternoon light that moves across the marble floor. The Roman Forum at golden hour, tourists gone home. The Trevi Fountain at midnight with room to breathe. The Rome experiences that belong to anyone willing to be there at the right time.",
("Best Things to Do in Rome (NEW)", "7"): "Cacio e pepe in a Trastevere trattoria that's been here since before you were born. A perfect espresso standing at a Roman bar for 1.20 euros. Artichokes fried Jewish-style in the Ghetto. Eating your way through Rome — the dishes, the neighborhoods, and the food experiences worth building a whole Italy trip around.",
("Best Things to Do in Rome (NEW)", "8"): "The Colosseum is worth it. The Vatican Museums are worth it (if you book). The catacombs are optional. An honest Italy travel guide to what Rome's biggest attractions are really like — the ones that earn the queue, the ones to skip, and the ones most first-timers accidentally miss.",

# ── Traveling With a Toddler ──────────────────────────────────────────────────
("Traveling With a Toddler", "1"): "The flight with a toddler is the part everyone dreads most. Here's what actually works: the packing list that fits in a carry-on, the timing tricks for overnight vs daytime flights, the jet-lag plan, and the one thing to do in the first hour that keeps everyone sane. Family travel tips for flying with young children.",
("Traveling With a Toddler", "2"): "The packing list for flying with a toddler. The in-flight tricks that actually work. The jet-lag plan for resetting small children across time zones. And the things no one tells you until you're already on the plane. Honest toddler travel tips from a parent who's done the long-haul with a two-year-old.",
("Traveling With a Toddler", "3"): "You can still travel the world with a toddler — you just travel differently. Slower pacing, earlier mornings, more snacks than you think you need. Here's how: the packing strategy, the flight survival guide, toddler-friendly accommodation, and managing jet lag with a small person who has no concept of time zones.",

# ── Zakynthos Road Trip Itinerary ─────────────────────────────────────────────
("Zakynthos Road Trip Itinerary", "1"): "The Navagio viewpoint above chalk-white cliffs, the Blue Caves lit turquoise from below, hidden west-coast coves, cliff-top tavernas with no printed menu. A Zakynthos road trip itinerary that covers the whole Greek island — day by day, with the best driving route, where to stop, and what to book in advance.",
("Zakynthos Road Trip Itinerary", "2"): "The drive that connects Navagio Shipwreck Beach, Porto Limnionas' rocky cove, and the south's Gerakas sea turtle beach in one circuit. A Zakynthos road trip route that earns every hour of driving — with the detours worth adding and the ones that waste your afternoon.",
("Zakynthos Road Trip Itinerary", "3"): "The Navagio viewpoint, the Blue Caves, the wine villages of the Zakynthos interior, and the best west-coast swims on the island. The Zakynthos road trip stops worth building your whole Greece island day around — a complete guide to renting a car and driving the island.",
("Zakynthos Road Trip Itinerary", "4"): "Cliff-top roads above turquoise water. The whole coastline laid out below the Navagio viewpoint. West-coast Greek island sunsets with no one else in sight. The most scenic Zakynthos road trip route — mapped so you catch the light at the right places and don't miss the best spots.",
("Zakynthos Road Trip Itinerary", "5"): "A rental car in Zakynthos unlocks the whole island in two days. Navagio viewpoint, the Blue Caves, Porto Limnionas, Gerakas sea turtle beach — the perfect Zakynthos circuit, mapped so nothing gets missed and the driving makes sense. Greece travel guide for island road trippers.",

# ── Where to Stay in Barcelona ────────────────────────────────────────────────
("Where to Stay in Barcelona", "4"): "Village squares in Gràcia. Art Nouveau architecture lining the Eixample boulevards. Medieval lanes threading through El Born. The Barcelona neighborhoods compared — Eixample, Gràcia, El Born, Gothic Quarter, Barceloneta — so you choose the one that actually suits the trip you're planning.",
("Where to Stay in Barcelona", "5"): "The smart Barcelona neighborhoods: close to Sagrada Família and the beach, not priced like Passeig de Gràcia hotels. Where to stay in Barcelona without paying Gaudí-monument prices — the best value areas for first-time visitors to Spain who want location and atmosphere in equal measure.",
("Where to Stay in Barcelona", "6"): "Barceloneta beach on your doorstep or Gothic Quarter wandering outside your window? How to choose your Barcelona base — Eixample, El Born, Barceloneta, Gràcia — what each area is really like and who each one suits for a first trip to Spain.",
("Where to Stay in Barcelona", "7"): "We stayed in the wrong Barcelona neighborhood on our first trip. Here's what we learned: avoid Las Ramblas hotels, book Eixample for a first visit, El Born if you're coming back. The honest Barcelona hotel location guide — Spain travel tips for smart first-timers.",

# ── Things to Do in São Miguel, Azores ───────────────────────────────────────
("Things to Do in São Miguel, Azores", "2"): "Sete Cidades is one of those places that genuinely lives up to the hype — twin crater lakes, one emerald green and one deep blue, surrounded by the walls of an ancient volcano. Sao Miguel, Azores' most beautiful landscape, and everything around it worth adding to your Portugal travel itinerary.",
("Things to Do in São Miguel, Azores", "3"): "Furnas is the most otherworldly corner of Sao Miguel — geothermal geysers bubble from the ground, food is slow-cooked in volcanic soil called cozido das Furnas, and the calderas steam at dawn. Everything to do in Furnas, Azores — a complete guide to this volcanic Portugal travel destination.",
("Things to Do in São Miguel, Azores", "4"): "Sao Miguel is the kind of place where you arrive for a long weekend and immediately start looking at flights to extend. Volcanic calderas at Sete Cidades, whale watching off Ponta Delgada, hot springs at Furnas, and black sand beaches on the Atlantic coast. The full guide to things to do in Sao Miguel, Azores.",
("Things to Do in São Miguel, Azores", "5"): "If you haven't heard of Sao Miguel yet, you will soon. This volcanic island in the mid-Atlantic has some of the most dramatic scenery in Europe — Sete Cidades crater lakes, Furnas geothermal valley, whale watching tours, and thermal pools. The complete things-to-do guide for the Azores main island, Portugal.",

# ── 5-Day New York City Itinerary ─────────────────────────────────────────────
("5-Day New York City Itinerary", "4"): "One neighborhood at a time: Midtown for the NYC icons, Lower Manhattan for the Brooklyn Bridge and history, Brooklyn Heights for the skyline views, the West Village for the food. A 5-day New York itinerary that uses the city the way locals do — without zigzagging across Manhattan.",
("5-Day New York City Itinerary", "5"): "Five days in New York: Central Park in the morning mist, the Brooklyn Bridge at golden hour, the skyline from a Williamsburg rooftop at night. The New York moments worth planning a trip around — plus a day-by-day itinerary for first-timers that fits it all in without exhausting yourself.",
("5-Day New York City Itinerary", "6"): "Central Park. The Brooklyn Bridge. The High Line. Chinatown. A Broadway show. Five days in New York City for first-timers — the complete itinerary that covers every icon without backtracking, with honest picks on what's worth it and what's overhyped.",
("5-Day New York City Itinerary", "7"): "The icons, the food neighborhoods, the views that stop you mid-sentence. A 5-day New York City itinerary that fits in Central Park, the Brooklyn Bridge at dawn, Chinatown, the High Line, and the skyline views — day by day, for first-timers visiting NYC.",
("5-Day New York City Itinerary", "8"): "The neighborhoods worth more of your time, the sights to skip, and the walking route that keeps your feet going in the right direction. Five days in New York without the regrets — honest picks from someone who knows which museum queues are worth the wait and which Broadway shows to book first.",

# ── Best Things to Do in Osaka ────────────────────────────────────────────────
("Best Things to Do in Osaka", "4"): "Dotonbori at midnight, neon reflecting on the canal, every takoyaki stall glowing and the city impossibly alive. The best evening things to do in Osaka — Japan's food capital that genuinely never sleeps. From Dotonbori street food to Namba nightlife to Shinsekai's retro charm.",

# ── Where to Stay in Amsterdam ────────────────────────────────────────────────
("Where to Stay in Amsterdam", "4"): "Smart Amsterdam neighborhoods close to the Rijksmuseum, Van Gogh Museum, and canal ring views — without Canal Ring hotel pricing. Where to stay in Amsterdam for first-timers when budget is part of the decision: De Pijp, Oud-West, and the neighborhoods locals actually live in.",

# ── Chicago Travel Costs ──────────────────────────────────────────────────────
("Chicago Travel Costs", "1"): "Chicago for two for four days — a Loop hotel, deep dish pizza at Lou Malnati's, the architecture river cruise, the Skydeck at sunset, a lakefront dinner. Here's exactly where every dollar went and what was genuinely worth it. A realistic Chicago travel budget for 2026.",
("Chicago Travel Costs", "2"): "Hotel in River North, deep dish pizza, the architecture river cruise, the Skydeck, and a lakefront dinner — a realistic Chicago trip cost, line by line, in 2026 prices. What to budget before you book, and where spending more actually makes a difference.",
("Chicago Travel Costs", "3"): "Chicago is cheaper than New York and more impressive than most people expect. Free museum days, a free lakefront, free parks. Here's how to stretch your Chicago travel budget — the smart swaps that cut the cost without skipping a single thing worth doing.",
("Chicago Travel Costs", "4"): "The architecture cruise is worth it. The Skydeck is worth it. The deep dish is worth it. Here's what to spend on in Chicago and what to do for free — a smarter Chicago budget breakdown for first-timers, with 2026 prices for everything on the itinerary.",

# ── 3 Days in Rome Itinerary ──────────────────────────────────────────────────
("3 Days in Rome Itinerary (VERIFY SLUG)", "5"): "The Colosseum is empty at 9am. The Vatican is manageable if you book the right tour and skip the standard one. A 3-day Rome itinerary timed around the quiet windows — so you see the Colosseum, the Pantheon, and Trastevere without the crush. Italy travel tips for first-timers.",
("3 Days in Rome Itinerary (VERIFY SLUG)", "6"): "Ivy on ancient walls, cobblestones underfoot, dinners in Trastevere that stretch past midnight. Trastevere isn't a detour in a Rome itinerary — it's the reason you stayed a third night and the neighborhood that makes Rome feel like yours. Italy travel guide for first-time visitors.",
("3 Days in Rome Itinerary (VERIFY SLUG)", "7"): "Rome rewards walking. The Colosseum to the Palatine Hill, the Roman Forum at golden hour, the Pantheon to the Trevi Fountain — a 3-day Rome route that connects all the icons without doubling back. The perfect first-timer Italy itinerary, day by day.",
("3 Days in Rome Itinerary (VERIFY SLUG)", "8"): "The Colosseum: book online or skip the queue. The Vatican: same rule. The Trevi Fountain: go after 10pm. The Rome tips that make a 3-day trip work — what to book in advance, what to skip, and what's actually worth your time in Italy's most visited city.",
("3 Days in Rome Itinerary (VERIFY SLUG)", "9"): "The Vatican at the wrong time, the Colosseum on a Tuesday without a skip-the-line ticket, Trastevere skipped for a nap. The Rome mistakes most first-timers make — and the 3-day itinerary that corrects all of them. Italy travel guide for people who want to do Rome properly.",

# ── Best Canal Cruises in Amsterdam ──────────────────────────────────────────
("Best Canal Cruises in Amsterdam", "2"): "Golden-hour bridges or canals lit at midnight? The case for booking an Amsterdam canal cruise in the evening — the light is softer, the crowds thinner, and the whole canal ring looks completely different after dark. Netherlands travel tips for the most romantic Amsterdam experience.",
("Best Canal Cruises in Amsterdam", "3"): "Amsterdam from the water looks nothing like Amsterdam from the street. The historic 17th-century bridges, the gabled facades reflected in the canal, the houseboats. The best Amsterdam canal cruises to see it all from the right angle — with honest recommendations for couples, families, and solo travelers.",
("Best Canal Cruises in Amsterdam", "4"): "Touristy or genuinely worth it? An honest take on Amsterdam canal cruises — which ones are worth the money, which to skip, and what the experience is actually like on a busy summer day. Netherlands travel tips before you book.",
("Best Canal Cruises in Amsterdam", "5"): "Wine, golden-hour bridges, and Amsterdam's canal ring at dusk with no crowds in sight. The canal cruises worth booking for couples — the small open boats that feel nothing like a tourist experience and everything like a private evening on the water. Netherlands travel guide.",
("Best Canal Cruises in Amsterdam", "6"): "A small intimate open boat or the classic glass-topped Amsterdam canal cruiser? How to choose the right canal cruise for your Netherlands trip — what each offers, what everything costs in 2026, and when to book for the best experience.",

# ── Best Time to Visit the Azores ────────────────────────────────────────────
("Best Time to Visit the Azores", "2"): "April to June: Azores whale watching peaks, the island of São Miguel turns blue-purple with hydrangeas, and the Sete Cidades hiking trails are nearly empty. The case for visiting the Azores in spring — and when the other seasons are genuinely worth considering for this Portugal Atlantic destination.",
("Best Time to Visit the Azores", "3"): "The Azores have a reputation for unpredictable weather — and it's partly earned. Here's how to read it: which months are reliably good for whale watching and hiking, which activities work in each season, and why the dramatic cloud-and-mist days sometimes create the most extraordinary Azores scenery.",

# ── Where to Stay in Chicago ──────────────────────────────────────────────────
("Where to Stay in Chicago", "4"): "Smart Chicago neighborhoods close to the architecture river cruise, Millennium Park, and the El train — without the Loop hotel premium. Where to stay in Chicago for first-timers: River North, the Gold Coast, Lincoln Park, and the neighborhoods that give you the city without the extra cost.",

# ── Free Things to Do in Marsa Alam ──────────────────────────────────────────
("Free Things to Do in Marsa Alam", "2"): "Coral straight off the beach with no boat required. Red Sea sunsets from the shore with dolphins visible at dusk. Desert evenings with zero light pollution and a Milky Way overhead. How to enjoy Marsa Alam's best Egypt travel experiences without adding a single euro to the resort bill.",

# ── Barcelona Travel Costs ────────────────────────────────────────────────────
("Barcelona Travel Costs", "1"): "Barcelona for two for a week — Sagrada Família tickets booked in advance, Park Güell, a hotel in the Eixample, tapas dinners in El Born, a beach afternoon in Barceloneta, a day trip to Montserrat. Here's exactly where every euro went and what was genuinely worth it. Spain travel budget 2026.",
("Barcelona Travel Costs", "2"): "Flights, an Eixample hotel, Gaudí attraction tickets, daily tapas and cava, a Montserrat day trip from Barcelona. A realistic Spain travel budget, line by line, in 2026 prices — so no number surprises you when you land.",
("Barcelona Travel Costs", "3"): "Barcelona is cheaper than Paris and more expensive than Lisbon — here's how to make it even cheaper: the free Gaudí views from outside, the local tapas bars where tourists don't go, and the Barcelona neighborhoods with good hotels at half the price of Las Ramblas.",
("Barcelona Travel Costs", "4"): "The Gaudí tickets worth buying in advance (Sagrada Família, Casa Batlló), the ones you can walk straight into, and the ones you can photograph from outside for free. A smarter Barcelona travel budget, experience by experience — Spain travel tips for 2026.",
("Barcelona Travel Costs", "5"): "What should you budget for Barcelona? Start with these real 2026 numbers: accommodation costs by neighborhood, daily food and drink, Gaudí attraction prices, and what a Montserrat day trip adds to the total. A Spain travel cost guide for first-time visitors.",

# ── Azores Whale Watching ─────────────────────────────────────────────────────
("Azores Whale Watching", "2"): "Whale watching in the Azores is not like whale watching anywhere else. The islands sit on a permanent cetacean feeding ground — shore spotters with binoculars locate the whales before your boat even leaves the harbor. Sperm whales, blue whales, common dolphins, all wild and all close. A Portugal travel guide for the best whale watching in Europe.",
("Azores Whale Watching", "3"): "If there's one place in Europe where whale watching genuinely lives up to the hype, it's the Azores. São Miguel has sperm whales year-round, blue whales in spring, and sightings on the vast majority of trips. What to expect, which Azores whale watching company to book with, and how to avoid seasickness.",
("Azores Whale Watching", "4"): "Whale watching in the Azores is the kind of experience that completely reframes what a wildlife encounter can be. The Azores are a whale superhighway between the Atlantic and the Med. How to book, the best time of year to go, what species you'll see, and what you'll actually experience on the water — Portugal travel guide.",

# ── 2 Days in Athens ──────────────────────────────────────────────────────────
("2 Days in Athens", "5"): "Treating Athens as a one-day stopover before the Greek islands is the biggest Greece itinerary mistake. Here's what you miss: the ancient Agora at golden hour with no one around, the Plaka's taverna dinners that stretch past midnight, and the rooftop bars with Parthenon views that justify staying the extra night.",
("2 Days in Athens", "6"): "Athens before the Greek islands — the Acropolis and Parthenon at dawn, the ancient Agora and Roman Forum below it, a Plaka dinner, a rooftop sunset with the Parthenon as your backdrop. The ideal 2-day Athens stopover that makes you wish you'd booked a third night. Greece travel guide for first-timers.",

# ── Chicago Bucket List ────────────────────────────────────────────────────────
("Chicago Bucket List", "5"): "Cloud Gate reflecting an infinite Chicago skyline. The architecture river cruise through the downtown canyon. Deep dish pizza at Lou Malnati's. The lakefront trail stretching 18 miles. Millennium Park on a summer evening. The Chicago bucket list for first-time visitors — honest about every experience.",
("Chicago Bucket List", "6"): "Chicago-style deep dish that requires both hands. An Italian beef sandwich, dipped. The Revival Food Hall on a lunch break. A lakefront patio at golden hour with the lake looking like an ocean. Eating your way through Chicago — the food experiences that earn their own USA travel bucket list.",
("Chicago Bucket List", "7"): "The architecture river cruise puts the whole Chicago skyline in context. Then you walk past those same buildings and recognize every one — the Tribune Tower, the Wrigley Building, Marina City. Why the river cruise tops every Chicago bucket list and what comes second: the full USA travel guide for first-timers.",

# ── Free Stopover Flights in 2026 ────────────────────────────────────────────
("Free Stopover Flights in 2026", "2"): "Iceland, Dubai, Singapore, Doha, Tokyo — the airlines that let you stop for days between flights, at no extra cost. The best free stopover programs in 2026, with how to search and book them, what each city lets you do in 48-72 hours, and the routes where they make the most sense.",
("Free Stopover Flights in 2026", "3"): "You're already on the flight. The stopover costs nothing extra on the ticket but adds a second country to the trip. How free stopover flights actually work, which airlines offer them in 2026 (Icelandair, Emirates, Singapore Airlines, Qatar Airways), and how to book it correctly so nothing falls through.",

# ── Amsterdam Travel Costs ────────────────────────────────────────────────────
("Amsterdam Travel Costs", "1"): "Amsterdam costs more than Prague and less than London — here's exactly what you'll spend. A canal-side Jordaan hotel, Van Gogh Museum tickets, a canal cruise at sunset, daily food and coffee, and transit, all broken down with real 2026 prices. The Netherlands travel budget guide that makes planning simple.",
("Amsterdam Travel Costs", "2"): "A realistic Amsterdam trip for two: a canal-view hotel in the Jordaan, the Van Gogh Museum, an evening canal cruise, daily Dutch food and coffee, and transit passes. What everything actually costs in Amsterdam in 2026, so no number comes as a surprise when you're planning your Netherlands travel budget.",
("Amsterdam Travel Costs", "3"): "Amsterdam on a budget is very doable if you know what to skip and what's surprisingly cheap. The free ferry across the IJ to the NDSM Wharf. The Albert Cuyp market for lunch. The Hortus Botanicus as a cheaper museum day. Smart Netherlands travel tips that save real money without missing anything that matters.",

# ── 9 Cheapest Countries to Visit ────────────────────────────────────────────
("9 Cheapest Countries to Visit", "1"): "Dinner for two with drinks for under 10 euros. A guesthouse with a mountain view for 25. That's not history — that's right now in Europe and Southeast Asia's most underrated destinations. The cheapest countries to visit in 2026 where your money actually feels like money again.",
("9 Cheapest Countries to Visit", "2"): "Where 50 euros a day buys you more than 200 does at home: the cheapest countries to visit right now, ranked by what flights, accommodation, and food actually cost in 2026. Budget travel destinations that aren't cheap for a reason — they're cheap because not enough people have found them yet.",
("9 Cheapest Countries to Visit", "3"): "Stunning landscapes, extraordinary food, almost no other tourists — and a fraction of what you'd pay in Spain or Italy. The cheapest countries to visit in 2026 that make your budget travel destination question easier to answer, with real current prices for accommodation, food, and getting around.",

# ── Amalfi Coast Travel Costs ─────────────────────────────────────────────────
("Amalfi Coast Travel Costs", "1"): "A week on the Amalfi Coast for two — here's exactly where every euro went. A hotel in Praiano, SITA bus passes, the Positano boat beach, a Capri day trip, lunches in Amalfi town, a Ravello evening. Is the Amalfi Coast worth the cost? Yes. Here's what to budget before you fall in love with it.",
("Amalfi Coast Travel Costs", "2"): "Hotel in Praiano, SITA ferries between towns, a Capri day trip, Positano lunches on a terrace, a boat rental to a hidden cove. The real Amalfi Coast travel costs broken down line by line in 2026 prices — so you know what to budget before you book Southern Italy.",
("Amalfi Coast Travel Costs", "3"): "The Amalfi Coast doesn't have to cost a fortune. Stay in Praiano instead of Positano — same views, half the price. Take the SITA cliff-road bus instead of the ferry. Here's how to cut the cost of a Southern Italy Amalfi trip without missing anything that actually matters.",
("Amalfi Coast Travel Costs", "4"): "The Capri day trip is worth it. The Ravello terrace dinner is worth it. The boat to Furore's hidden fjord is worth it. And the 5-euro SITA bus does the same cliff-road journey as a 40-euro ferry. A smarter Amalfi Coast travel budget — knowing where to spend and where to save.",

# ── Where to Stay in Tokyo ────────────────────────────────────────────────────
("Where to Stay in Tokyo", "1"): "Shinjuku is central and always buzzing. Shibuya is for nightlife and the famous crossing. Asakusa is for temples, senso-ji at dawn, and a quieter side of Tokyo. Ginza is expensive and convenient. The best Tokyo neighborhoods compared — the full breakdown for first-time Japan visitors choosing their hotel location.",
("Where to Stay in Tokyo", "2"): "Shinjuku or Shibuya — the two biggest Tokyo hotel questions for first-timers. What staying in each area is actually like, how well they connect to the rest of the city by subway, and which one suits your Japan itinerary. Japan travel guide for choosing the right Tokyo base.",
("Where to Stay in Tokyo", "3"): "Smart Tokyo neighborhoods with fast train access to Shibuya, Shinjuku, Asakusa, and lower prices than the big-name areas. Where to stay in Tokyo when location matters but so does the accommodation budget — Japan travel tips for first-timers who want to do it right.",

# ── 20 Free Things to Do in Chicago ──────────────────────────────────────────
("20 Free Things to Do in Chicago", "1"): "Chicago has a free Art Institute admission day, Lincoln Park Zoo (always free), an 18-mile lakefront trail, Millennium Park, and the Bean — all completely free. Here's how to spend a full Chicago day without spending a dollar, and what the free experience is actually like.",
("20 Free Things to Do in Chicago", "2"): "Millennium Park at golden hour, the Chicago Riverwalk at sunset, Lincoln Park Zoo on a quiet morning, and free museum admission Mondays. Chicago gives away more than most American cities charge for. The complete guide to free things to do in Chicago for first-time visitors.",
("20 Free Things to Do in Chicago", "3"): "The Bean is free. The lakefront is free. The beaches are free. Museum days are free if you time them right. So are the architecture walking tours, the neighborhood markets, and most of the parks worth exploring. How to do the best of Chicago without the bill — USA travel tips for budget travelers.",

# ── Where to Stay in Zakynthos ────────────────────────────────────────────────
("Where to Stay in Zakynthos", "1"): "Laganas for nightlife, sandy beach, and the party atmosphere. Zakynthos Town for local character, the harbor, and easy access to the whole island. The quiet north coast for the best Zakynthos beaches and zero crowds. The complete Zakynthos neighborhood guide — where to base your Greece island stay.",

# ── 14-Day Southern Italy Road Trip ──────────────────────────────────────────
("14-Day Southern Italy Road Trip", "1"): "Naples pizza at midnight, the Amalfi Coast at golden hour, Matera's cave dwellings at dawn, Puglia's trulli in Alberobello — a 14-day southern Italy road trip covering the most cinematic stretch of Europe. Route map, best stops, driving tips, and what to book months in advance included.",

# ── Day Trips from Rome (NEW) ─────────────────────────────────────────────────
("Day Trips from Rome (NEW)", "1"): "Tivoli's Villa d'Este gardens are 45 minutes from Rome and feel like a completely different world. Ostia Antica makes Pompeii look crowded. Orvieto sits on a volcanic cliff above the valley. The best day trips from Rome, ranked honestly by how worth the journey they actually are — Italy travel guide.",

# ── Milan to Dolomites Road Trip ─────────────────────────────────────────────
("Milan to Dolomites Road Trip", "1"): "The drive from Milan to the Dolomites runs through Lake Garda's vineyards, passes Bolzano's medieval center, and arrives at mountain scenery that justifies every kilometer. The Milan to Dolomites road trip mapped — best route, top stops, driving tips, and how to do the Northern Italy journey in a day or weekend.",

# ── Free Things to Do in NYC (NEW) ───────────────────────────────────────────
("Free Things to Do in NYC (NEW)", "1"): "The Staten Island Ferry gives you the best Manhattan skyline view for completely free. The Brooklyn Bridge walk costs nothing. Central Park has 843 acres of city to explore. The best free things to do in New York City — the list that makes every NYC travel budget go significantly further.",

# ── Ryokan in Japan What to Expect ───────────────────────────────────────────
("Ryokan in Japan What to Expect", "1"): "Tatami floors, a private onsen bath, a kaiseki dinner of 12 courses eaten in your yukata while kneeling at a low table. A traditional Japanese ryokan is unlike any hotel anywhere in the world — what to expect when you arrive, the etiquette not to get wrong, and how to book the right one for your Japan itinerary.",

# ── Amsterdam With a Toddler ──────────────────────────────────────────────────
("Amsterdam With a Toddler", "1"): "A canal boat at toddler height, where everything is water and bridges and ducks. The Artis Zoo on a quiet weekday morning. The Vondelpark playground with a stroopwafel from the market. Amsterdam with a little one is more fun than it sounds — a practical family travel guide to the Netherlands with young children.",
("Amsterdam With a Toddler", "2"): "The best toddler-friendly neighborhoods in Amsterdam, stroller-accessible canal tours that work with small children, and the parks that keep little ones entertained without exhausting the adults. Amsterdam with a toddler: the honest family travel guide to the Netherlands with practical tips that actually work.",

# ── Dolomites Day Trip from Venice ────────────────────────────────────────────
("Dolomites Day Trip from Venice", "2"): "The drive from Venice takes three hours and arrives at mountain scenery that looks like it belongs on a different planet entirely. An honest take on the Dolomites day trip from Venice — what you actually see in a day, what you miss without a second night, and whether it's worth reorganizing your Italy itinerary for.",
("Dolomites Day Trip from Venice", "3"): "Lago di Braies at dawn with the turquoise water catching the first light. Cortina d'Ampezzo's mountain peaks visible from the main square. The first sight of Tre Cime di Lavaredo through a mountain pass. A Dolomites day trip from Venice worth the early start — and the Northern Italy route that earns every minute.",
("Dolomites Day Trip from Venice", "4"): "One day in the Dolomites from Venice: guided tour (easier, no driving, no parking) or rental car (better views, your own pace). Where to go when you have just one day, what to skip when time is tight, and which Dolomites highlights are actually reachable from Venice.",
("Dolomites Day Trip from Venice", "5"): "Guided tour ease or your own car and your own pace through Northern Italy? How to decide which kind of Dolomites day trip from Venice suits your Italy itinerary — what each option looks like in practice, what everything costs, and what you'll actually experience in the mountains.",
("Dolomites Day Trip from Venice", "6"): "The turquoise lakes, the jagged Dolomites ridgelines, the flower meadows that look hand-painted — all a few hours from Venice. The Dolomites day trip from Venice that makes people check flight change fees so they can stay longer in Northern Italy.",
("Dolomites Day Trip from Venice", "7"): "The timing that makes the drive worthwhile, the first Dolomites stops that earn the three-hour journey from Venice, and the mountain views that make everything clear. A Dolomites day trip guide that doesn't waste a single hour of the Italian Alps — Northern Italy travel tips.",

# ── Hiking in the Dolomites ───────────────────────────────────────────────────
("Hiking in the Dolomites", "4"): "Lago di Braies: turquoise glacial water ringed by Dolomites peaks, the rowing boats out at dawn. Lago di Sorapis: a color you genuinely don't believe until you're standing in front of it. The quieter Dolomites lake hikes that most Italy visitors miss — and why they're worth the extra effort to reach.",
("Hiking in the Dolomites", "5"): "The jagged Seceda ridge rising above the Val Gardena valley. The Odle rock formations catching the early morning light. Alpe di Siusi's flower meadows stretching toward the peaks. The Dolomites viewpoints that belong on every serious hiker's list — and the Italy hiking trails that lead to them.",
("Hiking in the Dolomites", "6"): "Sleeping in a mountain rifugio at 2,500 meters, a hot dinner with the peaks visible from your bunk, waking up above the clouds with no other buildings in sight. How to plan a multi-day Dolomites hut-to-hut hike — the basics of building an Italian Alps trekking itinerary.",
("Hiking in the Dolomites", "7"): "Some Dolomites trails have gondola access to the starting point, rifugio restaurants with views halfway up, and meadow sections that work for non-hikers. The Italy hiking trails that keep both the serious trekker and the casual walker happy — Dolomites travel guide for mixed-ability groups.",
("Hiking in the Dolomites", "8"): "Trails that start from the gondola station so the altitude is already done. Meadow walks above 2,000 meters with Dolomites peak panoramas. Rifugio-to-rifugio easy routes that put anyone above the treeline without a serious climb. The best easy hiking in the Italian Alps — for every fitness level.",
("Hiking in the Dolomites", "9"): "The trails worth every hiking day you give them (Tre Cime, Seceda, Cadini di Misurina, Lago di Braies), the best months to walk them, and the gear that actually matters in high alpine terrain. The complete Dolomites hiking guide for first-time Italian Alps visitors — route by route.",

# ── Fall in New York City ──────────────────────────────────────────────────────
("Fall in New York City", "1"): "Central Park in mid-October: amber maples, golden elms, the Ramble lit from above like something from a film. Fall in New York City is the city at its absolute best — smaller crowds, beautiful foliage, the energy of a city that just got its favorite season back. When to go, where to see the best NYC fall colors, and what events are worth planning your trip around.",
("Fall in New York City", "2"): "The Village Halloween Parade on October 31st. Central Park at peak fall foliage. The New York Film Festival. The NYC Marathon in November. Fall is New York's most event-packed season — a NYC travel guide to what to plan around, what to book weeks in advance, and the best autumn weekends to visit.",
("Fall in New York City", "3"): "Summer tourists gone. Holiday chaos not yet arrived. October in New York City is the sweet spot — warm enough for the city's rooftop bars, peak foliage in Central Park, the Halloween Parade on the 31st, and restaurant reservations that were impossible to get all August. Honest NYC fall travel guide.",

# ── Japan Fall Foliage ────────────────────────────────────────────────────────
("Japan Fall Foliage", "1"): "Maples turning crimson in Kyoto's Arashiyama. Ginkgos going gold along Tokyo's Shinjuku Gyoen paths. The Nikko valleys on fire with red and orange. Japan's koyo fall foliage season is one of the most extraordinary autumn spectacles in the world — when to go, where to see it, and how to time your Japan trip right.",
("Japan Fall Foliage", "2"): "The koyo color front moves south through Japan from late October into December — Nikko peaks first, then Tokyo, then Kyoto and Osaka. How to time a Japan fall trip to catch peak foliage in each city — the week-by-week guide that means you see the color instead of arriving a week too late.",
("Japan Fall Foliage", "3"): "Smaller crowds than cherry blossom season. Temple gardens in Kyoto draped in red and gold maple. Autumn matsuri festivals, the clearest hiking weather of the year, the best Japanese food season. Japan in fall may be the country's single best time to visit — an honest Japan travel guide to visiting in autumn.",

# ── Japan Cherry Blossom Season ──────────────────────────────────────────────
("Japan Cherry Blossom Season", "1"): "Cherry blossom season in Japan lasts about 10 days per city — and the sakura peak shifts north as the weeks pass. When the blossoms peak in Kyoto, Tokyo, and Osaka, how to track the cherry blossom forecast, and how to time your Japan itinerary to catch all three without missing the window.",
("Japan Cherry Blossom Season", "2"): "Kyoto's Philosopher's Path lined with hundreds of cherry trees in bloom. Tokyo's Meguro River pink and reflecting in the water from bank to bank. Castle moats in Hirosaki circled with sakura. The best places to see Japan's cherry blossoms — and the exact weeks when the hanami season peaks in each city.",

# ── Shipwreck Beach Zakynthos ─────────────────────────────────────────────────
("Shipwreck Beach Zakynthos", "1"): "Navagio Shipwreck Beach is only reachable by boat — sheer white limestone cliffs 200 meters high on three sides, a rusting 1980s freighter half-buried in white sand, the water a blue so saturated it doesn't look real. Here's how to get there, which boat tour to take, and what to expect when you arrive.",
("Shipwreck Beach Zakynthos", "2"): "Sheer white cliffs, a rusted shipwreck visible from the cliff viewpoint above before you even reach the beach, impossibly blue Ionian water, and no way in except by sea. Everything to know about visiting Navagio Shipwreck Beach in Zakynthos — which boat to take, when to go, and what the experience is actually like.",
("Shipwreck Beach Zakynthos", "3"): "The Navagio crowds come in summer, the boat takes 20 minutes from the north coast, and the view from the cliff viewpoint is a completely different experience from the beach itself — both are worth doing. An honest guide to visiting Navagio Shipwreck Beach in Zakynthos, Greece.",

# ── European Summer Bucket List ───────────────────────────────────────────────
("European Summer Bucket List", "1"): "Amalfi Coast swims off hidden coves. Greek island ferry crossings at sunset. Mountain lakes in the Austrian Alps. Long Spanish beach evenings that start at 8pm. The European summer bucket list for anyone who needs a reason to book the flight — every destination worth adding to a warm-weather Europe travel itinerary.",
("European Summer Bucket List", "2"): "Sun-drenched Mediterranean coastlines, Greek island ferries, long dinners that start when the sun finally sets at 9pm. The best European summer destinations for the kind of trip that feels like it belongs in a film — a Europe travel guide for summer bucket list planning.",

# ── Where to Stay in the Dolomites ───────────────────────────────────────────
("Where to Stay in the Dolomites", "4"): "Waking up with the Dolomites peaks visible from your window, the only sound the cowbells from the valley below. The mountain stays where the view is the whole experience — guesthouses and rifugios in Val Gardena, Alta Badia, and Cortina d'Ampezzo positioned to wake you up above the Italian Alps.",
("Where to Stay in the Dolomites", "5"): "Family-run guesthouses, half-board dinners with the whole family at one long table, no-frills hiking village accommodation with trail access from the door. The Dolomites without the Cortina d'Ampezzo price tag — where to stay in Northern Italy for value and direct access to the best hiking trails.",
("Where to Stay in the Dolomites", "6"): "Gondolas at the end of the path. Playgrounds above 1,500 meters. Easy meadow trails with full Dolomites peak panoramas. The Italian Alps bases that work best for families with children — and what to book for a Dolomites trip with kids that keeps everyone happy.",

# ── Free Things to Do in Barcelona ───────────────────────────────────────────
("Free Things to Do in Barcelona", "1"): "The Bunkers del Carmel sunset costs nothing and beats every paid Barcelona viewpoint. The Gothic Quarter is free to wander. Park Güell's hillside terraces and Barceloneta beach require no ticket. A full Barcelona day — Spain travel tips for visitors who want to see everything without spending a euro.",

# ── Free Things to Do in Rome (NEW) ──────────────────────────────────────────
("Free Things to Do in Rome (NEW)", "1"): "The Pantheon entrance was free until 2023 — now it's 5 euros. Everything else on this Rome list is still completely free: the Trevi Fountain, the Spanish Steps, the Roman Forum exterior views, and the best free sunset in Rome from the Pincian Hill terrace. Italy travel tips for budget Rome visitors.",
("Free Things to Do in Rome (NEW)", "2"): "Fountains older than most countries. Piazzas designed in the Renaissance for lingering in. The Spanish Steps at golden hour with a gelato. How to spend a full day in Rome spending almost nothing — Italy travel tips that prove the Eternal City's greatest experiences don't require a ticket.",

# ── 25 Best Things to Do in NYC ───────────────────────────────────────────────
("25 Best Things to Do in NYC", "4"): "The High Line at dusk, with the Hudson River catching the last light. The West Village for dinner, where the streets are narrow and the restaurants are exactly right. Roosevelt Island for the city skyline views without the tourist crowds. New York's best-kept secrets for first-timers — the NYC spots locals love.",
("25 Best Things to Do in NYC", "5"): "Cherry blossoms in Central Park. The Brooklyn Bridge walk at golden hour. A Broadway show. The Manhattan skyline from the Staten Island Ferry at sunrise. The New York bucket list experiences that live up to every piece of hype they've ever received — NYC travel guide for first-timers.",
("25 Best Things to Do in NYC", "6"): "A perfect New York bagel in the Lower East Side. A Chinatown dumpling crawl for under 15 dollars. The Chelsea Market food hall. Eating your way through New York City — the food experiences worth planning an entire NYC travel day around.",
("25 Best Things to Do in NYC", "7"): "Central Park in any season. The Brooklyn Bridge at dawn. Grand Central's celestial ceiling caught in afternoon light. The Manhattan skyline from Top of the Rock at sunset. The most iconic New York moments, ranked honestly by someone who's done them all more than once — USA travel guide.",
("25 Best Things to Do in NYC", "8"): "Which New York City attractions are genuinely worth their price tag and which are tourist traps — an honest USA travel guide. The Brooklyn Bridge walk, Central Park, and the Staten Island Ferry are always worth it. The Empire State vs Top of the Rock debate, settled.",
("25 Best Things to Do in NYC", "9"): "The Brooklyn Bridge walk, Central Park's Bethesda Fountain, Grand Central's hidden Whispering Gallery, and the skyline views from the free Staten Island Ferry. The New York experiences that make first-timers understand the city's obsession — the real NYC bucket list, no filler.",

# ── Best Time to Visit the Dolomites ─────────────────────────────────────────
("Best Time to Visit the Dolomites", "1"): "The Dolomites in July: wildflowers carpeting the Alpine meadows below jagged limestone peaks. In September: golden larch trees turning the entire valleys amber. There's genuinely no bad time to visit Northern Italy's mountains — but there is a best season for what you want to do, and here's how to choose.",
("Best Time to Visit the Dolomites", "2"): "Open trails, manageable crowds compared to summer, the best hiking weather of the year, and larches starting to turn golden at the edges. The narrow window when the Dolomites are at their most beautiful — the best month to visit and what each Italian Alps season actually looks like.",

# ── Rome Travel Costs (NEW) ───────────────────────────────────────────────────
("Rome Travel Costs (NEW)", "1"): "A week in Rome for two — a Monti neighborhood hotel walking distance from the Colosseum, Colosseum skip-the-line tickets, Vatican Museums tour, daily espresso at 1.20 euros and pasta for lunch, transit passes. Here's where the money went, what was worth it, and what we'd skip next Italy trip.",
("Rome Travel Costs (NEW)", "2"): "Trastevere hotel, Colosseum entrance, Vatican skip-the-line tour, daily food, coffee, and transit in Rome. A realistic Italy travel budget for a week in Rome in 2026, line by line, so no number comes as a shock when you're planning the trip.",
("Rome Travel Costs (NEW)", "3"): "Rome on a budget is more doable than most Italian cities suggest. The Pantheon has free hours. The 1.20-euro espresso rule applies across the city. The neighborhoods with character and half-price hotels compared to the Vatican. Smart Italy travel tips that save real money in Rome without sacrificing anything worth doing.",

# ── NYC Travel Costs (NEW) ────────────────────────────────────────────────────
("NYC Travel Costs (NEW)", "1"): "A week in New York for two — a Midtown hotel, daily food across Manhattan, the MoMA and Met, a Broadway show, yellow taxis and Ubers. Here's exactly where every dollar went and what we'd cut next time. A realistic NYC travel budget for 2026 so you know what to plan for.",
("NYC Travel Costs (NEW)", "2"): "Hotel, daily New York food, museum passes, the subway, a Broadway show, and a rooftop dinner in Midtown. A realistic NYC travel budget, line by line, in 2026 prices — so you know what to plan for before you book flights to New York.",
("NYC Travel Costs (NEW)", "3"): "New York on a budget is absolutely possible. The free Staten Island Ferry with the best Manhattan skyline view. Free museum days at the Brooklyn Museum and Met. The 3-dollar pizza slice route across midtown. The smart swaps that bring a New York trip cost down without skipping a single thing worth doing.",
("NYC Travel Costs (NEW)", "4"): "The New York experiences worth paying for (the Broadway show, Top of the Rock, the Chelsea Market food hall) and the ones that are completely free (the Staten Island Ferry, the Brooklyn Bridge walk, Central Park). A smarter NYC travel budget breakdown for first-time visitors.",

# ── 3 Days in Chicago ─────────────────────────────────────────────────────────
("3 Days in Chicago", "4"): "The Bean is worth it. The architecture river cruise is worth it. The Skydeck glass ledge is worth it. Deep dish pizza on the Riverwalk is optional. An honest Chicago travel guide from someone who's stopped recommending the overhyped stops — and knows which experiences are genuinely the best in the city.",
("3 Days in Chicago", "5"): "Three Chicago days that earn every icon: Millennium Park and the Bean, the architecture river cruise, the Art Institute, the 18-mile lakefront trail and deep dish pizza to close the day. A Chicago weekend itinerary for first-time visitors that doesn't miss anything worth doing.",
("3 Days in Chicago", "6"): "The Skydeck ledge 1,353 feet above Chicago, the city stretching in every direction. The Chicago River lit gold at 6pm from the Riverwalk bridges. The lakefront path with Lake Michigan looking like an ocean. The Chicago viewpoints that make you understand why people move here and never leave — USA travel guide.",
("3 Days in Chicago", "7"): "The Bean, the Riverwalk, Millennium Park, the Magnificent Mile — Chicago's best sights are all connected on foot. A 3-day Chicago itinerary that links them in the right order so you walk less, see more, and end each day exactly where you want to be. USA travel guide for first-timers.",

# ── Best Things to Do in Marsa Alam ──────────────────────────────────────────
("Best Things to Do in Marsa Alam", "4"): "Sataya's wild spinner dolphins, Marsa Mubarak's sea turtles and dugongs, the coral gardens you can snorkel straight off the beach. How to see the Red Sea wildlife that makes Marsa Alam one of the best snorkeling destinations in the world — Egypt travel guide for first-time visitors.",
("Best Things to Do in Marsa Alam", "5"): "Snorkeling in a bay ringed by dolphins. A desert safari watching the Red Sea sunset from the dunes. Lazy beach days with nothing to do. The Marsa Alam experiences that make a week at the Red Sea go by far too fast — a bucket list Egypt travel guide for first-time Red Sea visitors.",
("Best Things to Do in Marsa Alam", "6"): "There's more beyond the resort pool: the house reef has sea turtles visible within minutes of putting your mask in. The Sataya day trip has 300 dolphins. The desert behind the coast glows red at sunset. The Marsa Alam Red Sea experiences worth leaving the sunlounger for.",
("Best Things to Do in Marsa Alam", "7"): "Elphinstone reef's vertical coral walls dropping into blue. Fury Shoal's shallow coral gardens. The Marsa Alam offshore dive sites compared by what you'll see, how deep they go, and how to reach them. The Egypt diving guide for serious underwater explorers visiting the Red Sea.",
("Best Things to Do in Marsa Alam", "8"): "Snorkeling in a lagoon of wild dolphins. A desert night under the Milky Way with no light for 50 miles. The Red Sea's clearest water over a coral reef visible from the surface. The Marsa Alam Egypt bucket-list experiences that make people book the same resort two years running.",

# ── Japan Travel Costs ────────────────────────────────────────────────────────
("Japan Travel Costs", "1"): "Japan is significantly more affordable than it looks once you factor in the JR Pass correctly. Accommodation in Tokyo, Japanese food costs (ramen for 7 euros, convenience store meals that are genuinely good), transport, and attractions: what a Japan trip actually costs in 2026, broken down honestly for first-time visitors.",

# ── Best Time to Visit Japan ──────────────────────────────────────────────────
("Best Time to Visit Japan", "1"): "Cherry blossoms in March and April. Fiery koyo maple season in November. The clean quiet of Japanese mountain winters. When to go to Japan depends entirely on what you want to experience — a Japan travel guide to every season and what each one offers for first-time and returning visitors.",

# ── Best Time to Visit Rome (NEW) ────────────────────────────────────────────
("Best Time to Visit Rome (NEW)", "1"): "October in Rome: Colosseum queues half the summer size, weather still warm enough for outdoor dinners, restaurant tables actually available without booking a month in advance, and the golden light that every Italy travel photographer makes the trip for. The best time to visit Rome — season by season, with honest tradeoffs.",

# ── Dolomites from Milan ──────────────────────────────────────────────────────
("Dolomites from Milan", "1"): "The drive from Milan to the Dolomites through Bolzano takes around three hours — and every kilometer of the mountain section looks better than the last. How to reach the Dolomites from Milan by car or train, what to do once you're there, and which Northern Italy route to take for the most dramatic entrance into the Italian Alps.",

# ── 24 Hours in Milan ─────────────────────────────────────────────────────────
("24 Hours in Milan", "1"): "Standing inside the Duomo, looking up at a ceiling that took 600 years to finish — that's how a Milan day starts. The Duomo rooftop walk, the Last Supper (book months ahead), the Brera district's gallery and aperitivo bars at golden hour. Everything worth doing in 24 hours in Milan — Italy travel guide for a tight stopover.",

# ── 16 Cheap Beach Destinations ───────────────────────────────────────────────
("16 Cheap Beach Destinations", "1"): "There are beaches with water so clear you can see the sandy bottom 10 meters down — and they don't cost a fortune to reach. The cheapest beach destinations in Europe and beyond that are actually worth the flight in 2026, with real current prices for accommodation, food, and getting there.",
("16 Cheap Beach Destinations", "2"): "White sand, turquoise water, and affordable flights — they exist in the same destination if you know where to look. The cheapest beach destinations worth traveling for in 2026, with honest numbers on what accommodation, food, and flights actually cost at each one.",

# ── Free Things to Do on the Amalfi Coast ────────────────────────────────────
("Free Things to Do on the Amalfi Coast", "1"): "The Path of the Gods coastal hike is completely free. Fornillo Beach doesn't charge an entry fee. The SITA cliff-road bus that connects Positano, Amalfi, and Ravello costs 2 euros. The Amalfi Coast has an entire category of free experiences most visitors don't think to look for — Italy travel tips.",
("Free Things to Do on the Amalfi Coast", "2"): "A clifftop hiking trail above the Tyrrhenian Sea. Wandering the car-free streets of Atrani, Scala, and Ravello. Cove swims below the limestone cliffs that nobody charges for. How to experience the best of the Amalfi Coast when you're trying to keep the Southern Italy travel budget down.",

}

# ── CSV update ────────────────────────────────────────────────────────────────
shutil.copy2(CSV_PATH, BACKUP)
print(f"Backup: {BACKUP}")

rows = []
with open(CSV_PATH, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f, delimiter=";")
    fieldnames = reader.fieldnames
    for row in reader:
        key = (row["Cikk"], row["Pin #"])
        if key in NEW_DESCRIPTIONS:
            row["Pin leiras"] = NEW_DESCRIPTIONS[key]
        rows.append(row)

with open(CSV_PATH, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=";")
    writer.writeheader()
    writer.writerows(rows)

updated = sum(1 for k in NEW_DESCRIPTIONS if any(
    r["Cikk"] == k[0] and r["Pin #"] == k[1] for r in rows
))
print(f"Frissitett sorok: {len(NEW_DESCRIPTIONS)} / {len(rows)} total")
print("Kesz!")

