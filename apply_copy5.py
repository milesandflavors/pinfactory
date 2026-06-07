# -*- coding: utf-8 -*-
"""Apply keyword-optimized copy for Amsterdam + Egypt/Marsa Alam + Planning clusters (final batch)."""
import csv, os

COPY = {
"3 Days in Amsterdam":[
("The perfect 3 days in Amsterdam","a first-timer's itinerary","3 Days in Amsterdam: The Perfect Itinerary","Canals, the Van Gogh Museum, the Jordaan and a canal cruise: a 3-day Amsterdam itinerary ordered so you see the best without rushing. Day-by-day with where to stay and what to book ahead."),
("Amsterdam in 3 days","exactly what to do each day","3-Day Amsterdam Itinerary: A Day-by-Day Plan","Three days in Amsterdam mapped out: the canal ring, the museums, the Jordaan, Vondelpark and a day trip. The day-by-day itinerary for first-time visitors."),
("First time in Amsterdam?","your no-stress 3-day route","3 Days in Amsterdam for First-Time Visitors","Where to stay, what to book ahead (Anne Frank House, Van Gogh), and the route that ties it together: a stress-free 3-day Amsterdam itinerary for first-timers."),
("Amsterdam's canals, museums & charm","in 3 perfect days","3 Days in Amsterdam: Canals, Museums & Charm","Golden-hour canals, world-class museums and the cozy Jordaan: the Amsterdam moments worth planning around, woven into a 3-day first-timer itinerary."),
],
"Amsterdam Bucket List":[
("The Amsterdam bucket list","for first-timers","Amsterdam Bucket List: Best Things to Do","Canal cruises, the Van Gogh Museum, the Jordaan and golden-hour bridges: the Amsterdam bucket list worth your time, ranked for first-timers. What's worth it and what to skip."),
("The most beautiful spots in Amsterdam","and how to see them","Most Beautiful Places in Amsterdam","The canal ring at golden hour, the Jordaan's bridges, tulip season and hidden courtyards: the most beautiful places in Amsterdam and how to see them. A first-timer's guide."),
("Amsterdam hidden gems","beyond the canals","Amsterdam Hidden Gems: Beyond the Tourist Trail","Quiet courtyards, local brown cafes, the Jordaan's backstreets and hidden museums: Amsterdam's hidden gems for travelers who want more than the canal ring."),
("First time in Amsterdam?","start with these must-dos","Best Things to Do in Amsterdam for First-Timers","A canal cruise, the Van Gogh Museum, the Jordaan and a bike ride: the Amsterdam must-dos that make a first trip click. The best things to do, ranked for first-time visitors."),
],
"Best Day Trips from Amsterdam":[
("The best day trips from Amsterdam","windmills, tulips & more","Best Day Trips from Amsterdam","Zaanse Schans windmills, Giethoorn's canals, Keukenhof tulips and historic Haarlem: the best day trips from Amsterdam, ranked, with how to get to each by train."),
("Tulips, windmills & fairytale villages","day trips from Amsterdam","Best Day Trips from Amsterdam: Tulips & Windmills","Keukenhof in bloom, the Zaanse Schans windmills and the canals of Giethoorn: the best day trips from Amsterdam and how to do them. For first-time visitors."),
("See the Dutch countryside","easy day trips from Amsterdam","Best Day Trips from Amsterdam by Train","Windmills, cheese towns and tulip fields a short train ride away: the easiest day trips from Amsterdam, with how to get there and when to go. A first-timer's guide."),
("Giethoorn & Zaanse Schans","the best Amsterdam day trips","Best Day Trips from Amsterdam: Giethoorn & Zaanse Schans","The car-free canal village of Giethoorn and the windmills of Zaanse Schans: two of the best day trips from Amsterdam, with how to visit and what to expect."),
],
"Where to Stay in Amsterdam":[
("Where to stay in Amsterdam","for first-time visitors","Where to Stay in Amsterdam for First-Time Visitors","The Canal Ring, the Jordaan, De Pijp or the center? The best Amsterdam neighborhoods compared, so you book the right area for your first trip. Honest pros, cons and what to avoid."),
("The Jordaan or the Canal Ring?","where to stay in Amsterdam","Where to Stay in Amsterdam: Jordaan vs Canal Ring","Cozy local charm or postcard canals? How to choose your Amsterdam base and what each trades off. The best neighborhoods to stay, compared for first-timers."),
("Don't book Amsterdam","before reading this neighborhood guide","Where to Stay in Amsterdam: The Neighborhood Guide","Before you book Amsterdam, read this: which neighborhood suits your trip, where it's worth paying more, and the areas to skip. The Canal Ring, Jordaan and De Pijp compared."),
("Amsterdam on a budget?","where to stay without overpaying","Where to Stay in Amsterdam on a Budget","Smart Amsterdam neighborhoods near the center without the high price tag: where to stay on a budget for a first trip. The best-value areas and honest tips."),
],
"Amsterdam Travel Costs":[
("Is Amsterdam expensive?","the honest answer, in real numbers","Amsterdam Travel Costs: An Honest Budget Guide","Is Amsterdam expensive? The honest answer in real numbers: hotels, food, museums and canal cruises. What an Amsterdam trip actually costs, with the swaps that bring it down."),
("What 3 days in Amsterdam cost us","euro by euro","What 3 Days in Amsterdam Actually Cost","A realistic Amsterdam trip, line by line: hotel, food, museums, a canal cruise and transit. What 3 days in Amsterdam actually cost us, plus where to save."),
("Amsterdam on a budget?","yes, here's how","Amsterdam on a Budget: How to Visit for Less","Amsterdam on a budget is doable. The big expenses and the smart swaps, from free ferries and parks to cheap eats. How to do Amsterdam for less without missing the canals."),
],
"Best Canal Cruises in Amsterdam":[
("The best canal cruise in Amsterdam","how to choose","Best Canal Cruises in Amsterdam: How to Choose","Day cruise, evening cruise or a small private boat? The best Amsterdam canal cruises compared, so you pick the right one. What each is like and what's worth the money."),
("Day or evening canal cruise?","the best of Amsterdam by boat","Best Canal Cruises in Amsterdam: Day vs Evening","Golden-hour bridges or the canals lit up at night? How to choose the best Amsterdam canal cruise for the experience you want. Compared for first-timers."),
("The most beautiful way to see Amsterdam","is by canal","Best Canal Cruises in Amsterdam: See the City by Boat","Amsterdam looks completely different from the water: the best canal cruises to see the bridges, the gabled houses and the golden-hour glow. Which to book and why."),
("Are Amsterdam canal cruises worth it?","the honest answer","Best Canal Cruises in Amsterdam: Are They Worth It?","Touristy or magical? An honest take on Amsterdam canal cruises, which are worth it, which to skip, and how to get the best experience on the water."),
("The best canal cruise for couples","romantic boats & sunsets","Best Romantic Canal Cruises in Amsterdam","Wine, golden-hour bridges and the canals at dusk: the best Amsterdam canal cruises for couples. Which to book for a romantic evening on the water."),
("Small boat or big cruise in Amsterdam?","how to pick","Best Canal Cruises in Amsterdam: Small Boat vs Big Cruise","Intimate open boats or the classic glass-top cruise? How to choose the best Amsterdam canal experience for your trip, with honest pros and cons."),
],
"Amsterdam With a Toddler":[
("Amsterdam with a toddler","what to know","Amsterdam With a Toddler: Tips & What to Do","Bikes, boats, playgrounds and toddler-friendly museums: how to enjoy Amsterdam with a little one, from getting around to where to stay. A parent's honest guide."),
("Visiting Amsterdam with kids?","here's how to do it","Amsterdam With a Toddler: A Parent's Guide","The toddler-friendly side of Amsterdam: parks, canal boats, the best areas to stay and how to handle the bikes and trams. Honest tips for a family trip."),
],
"Best Things to Do in Marsa Alam":[
("The best things to do in Marsa Alam","Red Sea paradise","Best Things to Do in Marsa Alam, Egypt","World-class snorkeling, dolphin reefs, desert trips and the Red Sea's clearest water: the best things to do in Marsa Alam, ranked for first-timers. What's worth it and what to skip."),
("Snorkeling in Marsa Alam","the best reefs","Best Things to Do in Marsa Alam: Snorkeling & Reefs","Sataya dolphin reef, Marsa Mubarak's turtles and dugongs, coral gardens off the beach: the best snorkeling in Marsa Alam and where to find it. A first-timer's Red Sea guide."),
("The most beautiful spots in Marsa Alam","Red Sea & desert","Most Beautiful Places in Marsa Alam, Egypt","Turquoise lagoons, coral reefs, desert dunes and starry nights: the most beautiful places in Marsa Alam and how to see them. A first-timer's guide to Egypt's Red Sea."),
("Swim with dolphins & turtles in Marsa Alam","here's how","Best Things to Do in Marsa Alam: Dolphins & Turtles","Sataya's wild dolphins, Marsa Mubarak's turtles and dugongs: how to ethically see Marsa Alam's marine life, plus the best reefs and trips. A first-timer's guide."),
("First time in Marsa Alam?","start with these must-dos","Best Things to Do in Marsa Alam for First-Timers","Snorkeling, a desert safari, dolphin reefs and lazy beach days: the Marsa Alam must-dos that make a first trip click. The best things to do, ranked for first-time visitors."),
("Beyond the resort in Marsa Alam","reefs, desert & dolphins","Best Things to Do in Marsa Alam Beyond the Resort","There's more than the pool: the reefs, desert safaris and dolphin trips worth leaving the resort for in Marsa Alam. A first-timer's guide to Egypt's Red Sea."),
("The best diving in Marsa Alam","reefs & dive sites","Best Things to Do in Marsa Alam: Diving & Dive Sites","Untouched coral, walls and the famous Elphinstone reef: the best diving and dive sites in Marsa Alam, plus what to know for first-timers on Egypt's Red Sea."),
("Marsa Alam bucket list","the can't-miss experiences","Marsa Alam Bucket List: The Best Experiences","Snorkeling with dolphins, a desert night under the stars, the Red Sea's clearest water: the Marsa Alam experiences worth building a trip around. For first-timers."),
],
"7 Days in Marsa Alam":[
("The perfect 7 days in Marsa Alam","a Red Sea itinerary","7 Days in Marsa Alam: The Perfect Itinerary","Snorkeling, dolphin reefs, a desert safari and pure beach time: a 7-day Marsa Alam itinerary that balances adventure and relaxation. Day-by-day with where to stay and what to book."),
("A week in Marsa Alam","exactly what to do","7 Days in Marsa Alam: A Day-by-Day Plan","Seven days on Egypt's Red Sea mapped out: the best reefs, a dolphin trip, a desert safari and lazy beach days. The day-by-day Marsa Alam itinerary for first-timers."),
("First time in Marsa Alam?","this 7-day plan does it all","7 Days in Marsa Alam for First-Timers","Where to stay, which trips to book, and how to balance reefs and rest: the 7-day Marsa Alam itinerary I wish I'd had. Snorkeling, dolphins and desert, done right."),
],
"Where to Stay in Marsa Alam":[
("Where to stay in Marsa Alam","best resorts & areas","Where to Stay in Marsa Alam, Egypt","All-inclusive resorts, house-reef hotels and quieter bays: where to stay in Marsa Alam for the trip you want. The best areas and resorts compared for first-timers."),
("The best house reefs in Marsa Alam","stay where you can snorkel","Where to Stay in Marsa Alam: Best House Reefs","Snorkel straight off the beach: the Marsa Alam resorts with the best house reefs, plus the areas to choose for coral and calm water. A first-timer's guide."),
("All-inclusive in Marsa Alam?","where to book","Where to Stay in Marsa Alam: Best All-Inclusive Resorts","The best all-inclusive resorts in Marsa Alam, compared by reef access, value and vibe: where to book for a Red Sea trip. Honest tips for first-timers."),
],
"Marsa Alam Travel Costs":[
("Is Marsa Alam expensive?","the honest answer","Marsa Alam Travel Costs: An Honest Budget Guide","Is Marsa Alam expensive? The honest answer in real numbers: resorts, trips, snorkeling and food. What a Marsa Alam trip actually costs, with the swaps that bring it down."),
("What a week in Marsa Alam costs","everything included","What 7 Days in Marsa Alam Actually Cost","A realistic Red Sea trip, line by line: flights, all-inclusive resort, snorkeling and desert trips. What a week in Marsa Alam actually costs, plus where to save."),
],
"Free Things to Do in Marsa Alam":[
("The best free things to do in Marsa Alam","beaches & reefs","Free Things to Do in Marsa Alam","Snorkeling the house reef, beach days, desert sunsets and starry nights: the best free things to do in Marsa Alam. How to enjoy Egypt's Red Sea between the paid trips."),
("Marsa Alam for free","reefs, beaches & stars","Free Things to Do in Marsa Alam, Egypt","Coral straight off the beach, endless Red Sea coastline and desert sunsets: how to enjoy Marsa Alam for free. The best no-cost things to do for a budget trip."),
],
"Best Travel Money Card":[
("The best travel money card","for 2026","Best Travel Money Card for 2026 (Compared)","No foreign-transaction fees, great exchange rates, free ATM withdrawals: the best travel money cards compared, so you stop losing money abroad. Honest picks for every kind of traveler."),
("Stop losing money abroad","the best travel cards compared","Best Travel Money Card: Stop Paying Fees Abroad","The hidden fees that quietly drain your trip budget, and the travel money cards that kill them. The best cards compared for fees, rates and ATM access."),
("Which travel card actually saves you money?","compared","Best Travel Money Card: Which One Saves You Most","Exchange rates, ATM fees and the fine print, compared: which travel money card actually saves you the most abroad. An honest, up-to-date guide for travelers."),
("The travel card every traveler needs","fee-free spending abroad","The Best Travel Money Card for Fee-Free Spending","Spend and withdraw abroad without the fees: the best travel money card for fee-free travel, plus how to use it and the traps to avoid. A traveler's honest guide."),
],
"9 Cheapest Countries to Visit":[
("The cheapest countries to visit","in 2026","9 Cheapest Countries to Visit in 2026","Big experiences, small budgets: the cheapest countries to visit right now, where your money goes furthest, and what a daily budget really looks like in each."),
("Travel more, spend less","the cheapest countries to visit","Cheapest Countries to Visit for Budget Travelers","Where flights, food and stays cost a fraction of home: the cheapest countries to visit, ranked, with real daily budgets. For travelers who want more trips for less."),
("Your money goes furthest here","the cheapest countries to travel","9 Cheapest Countries to Travel in 2026","Stunning, affordable and worth the flight: the cheapest countries to travel in 2026, with what you'll spend per day and why each is worth it."),
],
"European Summer Bucket List":[
("The ultimate European summer bucket list","where to go","European Summer Bucket List: Where to Go","Amalfi swims, Greek islands, Spanish beaches and alpine lakes: the European summer bucket list worth planning around. The best places to go and when, for an unforgettable summer."),
("Your dream European summer","the bucket list","European Summer Bucket List: Dream Destinations","Sun-drenched coasts, island ferries and long Mediterranean dinners: the European summer bucket list to plan your trip around. The most beautiful places to go this summer."),
],
"Free Stopover Flights in 2026":[
("How to get a free stopover flight","two trips for one","Free Stopover Flights: Two Destinations for One","Turn one flight into two trips: the airlines that offer free stopovers, how to book them, and the best routes to try in 2026. A traveler's guide to seeing more for less."),
("See two countries for the price of one","free stopover flights","Free Stopover Flights in 2026: How to Book","Iceland, Dubai, Singapore and more: the airlines with free stopover programs and how to use them to add a destination for free. The 2026 guide."),
("The travel hack that adds a free trip","stopover flights","Free Stopover Flights: The Hack That Adds a Trip","Add a few days in another city for free on the way to your destination: how free stopover flights work, which airlines offer them, and how to book. A smart-traveler guide."),
],
"How to Book Hotels Like a Pro":[
("How to book hotels like a pro","and pay less","How to Book Hotels Like a Pro (and Pay Less)","The booking tricks that get you better rooms for less: when to book, where to look, and how to score upgrades. A traveler's honest guide to booking hotels smarter."),
("Stop overpaying for hotels","book like a pro","How to Book Hotels and Stop Overpaying","The fees, the timing and the sites that quietly cost you more, and how to book hotels the smart way. Get a better room for less on your next trip."),
("The hotel booking secrets","that save you money","Hotel Booking Tips: Secrets to Save Money","Free upgrades, the best booking day, and the loyalty tricks that work: the hotel booking secrets that save real money. A traveler's guide to booking like a pro."),
],
"How to Find Cheap Flights":[
("How to find cheap flights","the real tricks that work","How to Find Cheap Flights (Real Tricks That Work)","When to book, the tools to use, and the myths to ignore: how to find cheap flights that actually work. A traveler's honest guide to flying for less."),
("Stop overpaying for flights","find them cheap","How to Find Cheap Flights and Stop Overpaying","The booking timing, the alerts and the search tricks that cut airfare: how to find cheap flights every time. A smart traveler's guide to flying for less."),
("The cheap flight secrets","airlines don't advertise","How to Find Cheap Flights: Secrets Airlines Don't Share","Error fares, flexible-date tricks and the best booking windows: the cheap-flight secrets that save real money. How to find cheap flights for your next trip."),
],
"How to Plan a Trip":[
("How to plan a trip","step by step","How to Plan a Trip: A Step-by-Step Guide","From idea to itinerary without the overwhelm: how to plan a trip step by step, from budgeting and booking to building a day-by-day plan. A traveler's complete guide."),
("Trip planning, made simple","the step-by-step guide","How to Plan a Trip the Easy Way","The exact steps to plan any trip, in order: dates, budget, flights, stays and itinerary. How to plan a trip without the stress, even if you've never done it before."),
("Plan your dream trip","without the overwhelm","How to Plan a Trip Without the Overwhelm","Where to start, what to book first, and how to build an itinerary that flows: the stress-free way to plan your dream trip. A step-by-step guide for any destination."),
],
"Traveling With a Toddler":[
("Traveling with a toddler","tips that actually work","Traveling With a Toddler: Tips That Actually Work","Flights, packing, jet lag and keeping everyone sane: the toddler travel tips that actually work, from a parent who's been there. How to travel with a little one and enjoy it."),
("Flying with a toddler?","here's how to survive it","Flying With a Toddler: How to Survive the Trip","The packing list, the flight tricks and the jet-lag plan: how to fly with a toddler and keep your sanity. Honest tips for traveling with a little one."),
("Travel doesn't stop with kids","toddler travel tips","Traveling With a Toddler: A Parent's Honest Guide","You can still travel with a toddler, here's how. Packing, flights, accommodation and managing the days, with the honest tips that make family trips work."),
],
"eSIM for Travel":[
("How to use an eSIM for travel","stay connected for less","eSIM for Travel: How to Stay Connected for Less","Skip roaming fees and pricey SIM cards: how an eSIM works, the best ones for travel, and how to set it up before you fly. A traveler's honest guide."),
("Stop paying roaming fees","use a travel eSIM","eSIM for Travel: Ditch the Roaming Fees","Cheap data the moment you land, no SIM swap needed: how a travel eSIM works and which ones are worth it. The fee-free way to stay connected abroad."),
("The travel eSIM guide","for stress-free data abroad","eSIM for Travel: The Complete Guide","What an eSIM is, how to set it up, and the best ones for travel: the complete guide to stress-free data abroad. Stay connected without the roaming bill."),
],
"16 Cheap Beach Destinations":[
("The cheapest beach destinations","for 2026","16 Cheap Beach Destinations for 2026","Turquoise water without the price tag: the cheapest beach destinations worth the flight, with what you'll spend and why each made the list. For budget beach lovers."),
("Dreamy beaches on a budget","the cheapest destinations","Cheap Beach Destinations: Paradise on a Budget","Where to find white sand and clear water without overspending: the cheapest beach destinations, ranked, with real daily budgets. Paradise for less."),
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
