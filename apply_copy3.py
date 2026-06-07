# -*- coding: utf-8 -*-
"""Apply keyword-optimized copy for Greece/Zakynthos/Athens + NYC clusters."""
import csv, os

COPY = {
"12-Day Greece Itinerary":[
("The perfect 12 days in Greece","islands, Athens & beaches","12-Day Greece Itinerary: The Perfect First Trip","Athens, Santorini, the islands and the beaches between: a 12-day Greece itinerary that balances ancient sights with island time. Day-by-day with ferries, where to stay, and how to island-hop without rushing. Your complete first-timer guide to Greece."),
("Greece in 12 days","exactly which islands to pick","12-Day Greece Itinerary: Which Islands to Choose","Santorini for the views, Naxos for the beaches, Athens for the history: how to choose your islands and tie them together in 12 days. The day-by-day Greece itinerary that makes the ferries make sense."),
("Athens, Santorini & the islands","12 unforgettable days in Greece","12 Days in Greece: Athens, Santorini & Island-Hopping","The Acropolis, the Santorini caldera, hidden island coves: a 12-day Greece itinerary built around the icons and the beaches. Where to go, how long to stay, and the ferry route that works."),
("First time in Greece?","this 12-day route does it all","12-Day Greece Itinerary for First-Timers","Where to start, which islands to pick, and how the ferries work: the 12-day Greece itinerary I wish I'd had on my first trip. Athens, Santorini and the beaches, in an order that flows."),
("The Greek islands worth your time","mapped into 12 days","12 Days in Greece: The Best Islands to Visit","Santorini, Naxos, Milos, Paros: the Greek islands worth your days and how to string them together in 12. The ferry-smart itinerary for a first trip to Greece."),
("Skip the tourist traps in Greece","do this 12-day route instead","12-Day Greece Itinerary: Beyond the Crowds","The icons worth it (Acropolis, Santorini sunset) plus the quieter islands most first-timers miss. A 12-day Greece itinerary that mixes the must-sees with the calm."),
("Santorini sunsets & hidden coves","12 days in Greece, done right","12 Days in Greece: Sunsets, Beaches & Ancient Sights","Caldera sunsets, turquoise coves and the Acropolis at golden hour: the Greece moments worth planning around, woven into a 12-day island-hopping itinerary for first-timers."),
("How to island-hop Greece","the 12-day ferry route that works","12-Day Greece Itinerary: The Island-Hopping Route","Which ferries, in what order, and how long on each island: the 12-day Greece island-hopping route that actually works. Athens, Santorini, Naxos and more, mapped day by day."),
("The Greece trip of a lifetime","in 12 perfect days","12 Days in Greece: The Trip of a Lifetime","Ancient Athens, white-and-blue islands, beaches you won't believe: the 12-day Greece itinerary that delivers the trip of a lifetime. Where to go, where to stay, and what not to miss."),
],
"2 Days in Athens":[
("The perfect 2 days in Athens","a first-timer's itinerary","2 Days in Athens: The Perfect Itinerary","The Acropolis, the Plaka, ancient ruins and rooftop sunsets: 2 days in Athens, mapped so you see the best without rushing. Day-by-day with where to eat, where to stay, and what not to miss."),
("Athens in 2 days","exactly what to do","2 Days in Athens: A Day-by-Day Plan","Two days in Athens done right: the Acropolis and Parthenon, the Plaka's lanes, the markets and a rooftop sunset over the ruins. The day-by-day itinerary for first-time visitors."),
("Is 2 days in Athens enough?","here's how to make it count","2 Days in Athens: How to Make It Count","Yes, you can do Athens well in 2 days. The Acropolis, the ancient Agora, the Plaka and the best rooftop views, in a route that flows. A first-timer's Athens itinerary."),
("The Acropolis at opening","start your 2 days in Athens here","2 Days in Athens: Beat the Crowds at the Acropolis","Go early and the Acropolis is almost yours: a 2-day Athens itinerary timed around the quiet windows, plus the Plaka, the Agora and a sunset rooftop. For first-time visitors."),
("First time in Athens?","your stress-free 2-day route","2 Days in Athens for First-Time Visitors","Where to stay, what to book, and the walking route that ties it together: a stress-free 2-day Athens itinerary. The Acropolis, the Plaka and the best food, in an order that works."),
("Athens in 2 days, then the islands","the perfect Greece starter","2 Days in Athens Before the Islands","The ideal Athens stopover before island-hopping: the Acropolis, the Plaka and a rooftop sunset in 2 well-planned days. How to start a Greece trip right."),
],
"Best Beaches in Zakynthos":[
("The most beautiful beaches in Zakynthos","ranked","Best Beaches in Zakynthos, Greece (Ranked)","Navagio Shipwreck Beach, the Blue Caves, turquoise coves you reach by boat: the most beautiful beaches in Zakynthos, ranked, with how to get to each. Your guide to the island's best swims."),
("Navagio Shipwreck Beach & beyond","the best beaches in Zakynthos","Best Beaches in Zakynthos: Navagio & Hidden Coves","The famous Shipwreck Beach plus the quieter coves locals love: the best beaches in Zakynthos and how to reach them. The turquoise-water guide for your Greek island trip."),
("The bluest water in Greece","is in Zakynthos","Best Beaches in Zakynthos: Greece's Bluest Water","Navagio, the Blue Caves, Porto Limnionas: the Zakynthos beaches with the most unreal turquoise water in Greece. Where to swim and how to get there, mapped for first-timers."),
("Zakynthos beaches you can drive to","no boat needed","Best Beaches in Zakynthos You Can Drive To","Skip the boat: the best Zakynthos beaches you can reach by car, from Gerakas to Porto Limnionas. Where to park, what to expect, and the turquoise swims worth the drive."),
("The Zakynthos beach worth the boat trip","Navagio & the Blue Caves","Best Beaches in Zakynthos: Navagio by Boat","Navagio Shipwreck Beach and the Blue Caves are only reachable by sea, and worth every minute. How to do the Zakynthos boat trip and the beaches to pair with it."),
("Where to swim in Zakynthos","the best beaches, sorted","Best Beaches in Zakynthos for Every Traveler","Family sands, snorkeling coves, dramatic cliffs: the best beaches in Zakynthos sorted by what you want. From Navagio to Gerakas, the turquoise-water guide for a first trip."),
("Turtle beaches & turquoise coves","the best of Zakynthos","Best Beaches in Zakynthos: Turtles & Turquoise","Loggerhead turtles at Gerakas, the Blue Caves, Navagio's cliffs: the Zakynthos beaches that make the island unforgettable. Where to go and how to get there."),
("The Zakynthos beach bucket list","every swim worth it","Best Beaches in Zakynthos: The Beach Bucket List","Navagio, the Blue Caves, Porto Limnionas, Gerakas: the Zakynthos beaches worth building a trip around. The complete best-beaches guide for Greece's most beautiful island."),
],
"Zakynthos Road Trip Itinerary":[
("The perfect Zakynthos road trip","beaches, caves & viewpoints","Zakynthos Road Trip Itinerary: The Perfect Route","Navagio viewpoint, the Blue Caves, hidden beaches and cliff-top tavernas: a Zakynthos road trip that links the island's best in the right order. Where to drive, stop and swim."),
("How to see Zakynthos by car","the best route","Zakynthos Road Trip: How to See the Island by Car","The drive that connects Navagio, Porto Limnionas and the south's turtle beaches: a Zakynthos road trip itinerary with where to park and what to skip. For first-time visitors."),
("Zakynthos by car","the can't-miss stops","Zakynthos Road Trip Itinerary: The Best Stops","The Navagio viewpoint, the Blue Caves, the wine villages and the best swims: the can't-miss stops on a Zakynthos road trip, mapped into an easy driving route."),
("The Zakynthos drive with the best views","cliffs, coves & sunsets","Zakynthos Road Trip: The Most Scenic Route","Cliff-top viewpoints, turquoise coves and west-coast sunsets: the most scenic Zakynthos road trip, stop by stop. How to drive the island and where to stop for the views."),
("Renting a car in Zakynthos?","here's the perfect route","Zakynthos Road Trip Itinerary (+ Car Tips)","Got a car in Zakynthos? The perfect route around the island: Navagio, the Blue Caves, Porto Limnionas and the turtle beaches, with honest driving and parking tips."),
],
"Shipwreck Beach Zakynthos":[
("How to visit Shipwreck Beach","Zakynthos' famous Navagio","How to Visit Shipwreck Beach (Navagio), Zakynthos","Navagio Shipwreck Beach is Greece's most photographed cove, and only reachable by boat. How to visit, the best viewpoint, when to go, and the boat trips that take you there."),
("The most famous beach in Greece","Navagio, Zakynthos","Shipwreck Beach Zakynthos: Everything to Know","Sheer white cliffs, a rusting wreck, impossibly blue water: everything to know about visiting Navagio Shipwreck Beach in Zakynthos, from the viewpoint to the boat trips."),
("Is Shipwreck Beach worth it?","the honest answer","Shipwreck Beach Zakynthos: Is It Worth It?","The crowds, the boat trip, the jaw-dropping view: an honest take on visiting Navagio Shipwreck Beach in Zakynthos, plus the best time to go and how to beat the crowds."),
],
"Where to Stay in Zakynthos":[
("Where to stay in Zakynthos","best areas for your trip","Where to Stay in Zakynthos: Best Areas & Towns","Laganas for nightlife, Zakynthos Town for charm, the quiet north for beaches: where to stay in Zakynthos for the trip you want. The best areas compared for first-timers."),
],
"25 Best Things to Do in NYC":[
("The best things to do in NYC","ranked for first-timers","25 Best Things to Do in NYC for First-Timers","Central Park, the Brooklyn Bridge, the skyline views and the food: the best things to do in New York City, ranked honestly for first-timers. What's worth it, what to skip, and how to fit it in."),
("First time in NYC?","start with these must-dos","Best Things to Do in NYC for First-Time Visitors","The New York must-dos that make a first trip click: Times Square, Central Park, the Brooklyn Bridge and the best skyline views. The best things to do, ranked for first-timers."),
("The best NYC views","and where to find them","Best Things to Do in NYC: The Best Skyline Views","Top of the Rock, the Edge, the Brooklyn Bridge at golden hour: the best New York City skyline views and when to go. The can't-miss viewpoints for a first NYC trip."),
("NYC hidden gems","beyond Times Square","NYC Hidden Gems: Beyond the Tourist Spots","The High Line, the West Village, Roosevelt Island and the best local eats: New York's hidden gems for travelers who want more than Times Square. The best things to do off the beaten path."),
("The most iconic NYC moments","you have to experience","Best Things to Do in NYC: The Iconic Experiences","Central Park in fall, the Brooklyn Bridge at dawn, a Broadway show, the skyline from the water: the most iconic New York moments worth planning a trip around."),
("Eat your way through NYC","the food worth traveling for","Best Things to Do in NYC: The Food Worth Traveling For","Bagels, pizza slices, dumplings and the best food halls: eating your way through New York City. A first-timer's food guide to the best bites in NYC."),
("The most beautiful spots in NYC","and when to see them","Most Beautiful Places in NYC (+ Best Times)","Central Park, the Brooklyn Bridge, Grand Central and the skyline at golden hour: the most beautiful places in New York City and when to see them. A first-timer's guide."),
("Worth it or overrated in NYC?","an honest first-timer take","Best Things to Do in NYC: Worth It or Overrated?","An honest take on New York's big attractions: which ones earn your time and which to skip. From the Empire State to Times Square, the best things to do, ranked for first-timers."),
("NYC bucket list","25 things to do at least once","NYC Bucket List: 25 Things to Do at Least Once","Central Park, the Brooklyn Bridge, a Broadway show, the skyline from the water: the New York bucket list worth building a trip around. 25 best things to do for first-timers."),
],
"5-Day New York City Itinerary":[
("The perfect 5 days in NYC","a first-timer's itinerary","5 Days in New York City: The Perfect Itinerary","Manhattan icons, Brooklyn views, Central Park and the best food: a 5-day NYC itinerary ordered by neighborhood so you walk less and see more. Day-by-day with where to stay and what to book."),
("NYC in 5 days","exactly what to do each day","5-Day New York City Itinerary: A Day-by-Day Plan","Five days in New York mapped by neighborhood: Midtown icons, Lower Manhattan, Brooklyn, the Upper East Side and the Village. The day-by-day NYC itinerary for first-timers."),
("First time in NYC?","your no-stress 5-day route","5 Days in NYC for First-Time Visitors","Where to stay, how to use the subway, and what to prioritize: a stress-free 5-day New York itinerary. Central Park, the Brooklyn Bridge, the skyline and the food, in an order that flows."),
("NYC by neighborhood in 5 days","the smart way to see it","5-Day NYC Itinerary: Neighborhood by Neighborhood","See New York the smart way, one neighborhood at a time: Midtown, Lower Manhattan, Brooklyn, the Village and uptown. A 5-day itinerary that cuts the backtracking."),
("5 days in NYC, no wasted time","the itinerary that works","5 Days in New York: The Itinerary That Works","No zigzagging across the city: the 5-day New York itinerary that just works, grouped by area. The icons, the views and the food, mapped for first-time visitors."),
("Central Park to the Brooklyn Bridge","NYC in 5 perfect days","5 Days in NYC: Icons, Views & Neighborhoods","Central Park mornings, skyline sunsets, Brooklyn Bridge at golden hour: the New York moments worth planning around, woven into a 5-day first-timer itinerary."),
("The NYC trip that does it all","in 5 days","5 Days in New York City: See It All","Icons, food, views and the neighborhoods that make New York: a 5-day itinerary that fits it all without burning out. Where to stay, what to book, what to skip."),
("What I'd do with 5 days in NYC","a smarter itinerary","5 Days in NYC: A Smarter Itinerary","The neighborhoods worth more time, the sights to skip, and the order that saves your feet: a smarter 5-day New York itinerary, built from experience, for first-timers."),
],
"Where to Stay in NYC (NEW)":[
("Where to stay in NYC","for first-time visitors","Where to Stay in NYC for First-Time Visitors","Not sure where to stay in New York? Midtown, the Village, the Lower East Side and Brooklyn compared, so you book the right area for your first trip. Honest pros, cons and what to avoid."),
("Don't book NYC","before reading this neighborhood guide","Where to Stay in NYC: The Neighborhood Guide","Before you book New York, read this: which neighborhood suits your trip, where it's worth paying more, and the areas to skip. Midtown, Downtown and Brooklyn compared for first-timers."),
("Manhattan or Brooklyn?","where to stay in NYC","Where to Stay in NYC: Manhattan vs Brooklyn","Central Manhattan convenience or Brooklyn cool and value? How to choose your New York base and what each trades off. The best areas to stay, compared for first-timers."),
("NYC on a budget?","where to stay without overpaying","Where to Stay in NYC on a Budget","Smart New York neighborhoods that keep you near the subway without the Midtown price tag. Where to stay on a budget for a first trip, with the best-value areas and honest tips."),
],
"NYC Travel Costs (NEW)":[
("Is NYC expensive?","the honest answer, in real numbers","NYC Travel Costs: An Honest Budget Guide","Is New York expensive? The honest answer in real numbers: hotels, food, attractions and the subway. What an NYC trip actually costs, with the swaps that bring it down. A realistic budget guide."),
("What 5 days in NYC cost us","dollar by dollar","What 5 Days in NYC Actually Cost","A realistic New York trip, line by line: hotel, food, attractions, subway and a Broadway show. What 5 days in NYC actually cost us, plus where to save without missing the magic."),
("NYC on a budget?","yes, it's possible","New York on a Budget: How to Visit for Less","New York on a budget is possible. The big expenses and the smart ways around them, from free views and parks to cheap eats. How to do NYC for less without missing the icons."),
("Where to splurge, where to save","in New York City","NYC Travel Costs: Where to Splurge and Save","The New York experiences worth paying for and the ones to do free: a smarter way to budget your trip. Hotels, food, attractions and transit, with honest splurge-or-skip calls."),
],
"Free Things to Do in NYC (NEW)":[
("The best free things to do in NYC","that still feel iconic","Free Things to Do in NYC That Still Feel Iconic","The Brooklyn Bridge, Central Park, the Staten Island Ferry skyline and the High Line: the best free things to do in New York that still feel like the real thing. How to do NYC without spending."),
],
}

ROOT = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.reader(open(os.path.join(ROOT, "pins.csv"), encoding="utf-8-sig"), delimiter=";"))
h = {n: i for i, n in enumerate(rows[0])}
cnt = {}
for r in rows[1:]:
    a = r[h["Cikk"]]
    if a in COPY:
        i = int(r[h["Pin #"]]) - 1
        if i < len(COPY[a]):
            b, l, t, d = COPY[a][i]
            r[h["Pin bold (vastag)"]] = b; r[h["Pin light (vekony)"]] = l
            r[h["Pin cim"]] = t; r[h["Pin leiras"]] = d
            cnt[a] = cnt.get(a, 0) + 1
with open(os.path.join(ROOT, "pins.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(rows[0]); w.writerows(rows[1:])
print("Updated:", sum(cnt.values()), "pins across", len(cnt), "articles")
for a in cnt: print(f"   {cnt[a]:>2}  {a}")
