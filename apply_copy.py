# -*- coding: utf-8 -*-
"""Apply keyword-optimized copy (hook bold/light + SEO title + description) to pins.csv per article."""
import csv, os, sys

COPY = {
"Barcelona Bucket List":[
("Barcelona First Timer?","the bucket list that's actually worth it","Barcelona Bucket List: 25 Best Things to Do for First-Timers","Gaudi, the Gothic Quarter, tapas and the beach: the Barcelona bucket list that's genuinely worth your time, ranked honestly for first-time visitors. From Sagrada Familia and Park Guell to the sunset spots locals love, with what's worth it and what to skip. Your complete first-timer guide to Barcelona, Spain."),
("The most beautiful spots in Barcelona","and how to see them in one trip","The Most Beautiful Places in Barcelona, Spain","From Gaudi's Sagrada Familia and Park Guell to the Bunkers del Carmel sunset and the Gothic Quarter's hidden squares: the most beautiful places in Barcelona, and how to fit them into one trip. A first-timer's guide to the city's most photogenic spots."),
("Sagrada Familia, Park Guell & beyond","your complete Barcelona bucket list","Barcelona Bucket List: Sagrada Familia, Park Guell & More","The Gaudi icons everyone comes for, Sagrada Familia, Park Guell, Casa Batllo, plus the tapas streets, beaches and viewpoints that make Barcelona unforgettable. Your complete bucket list for a first trip to Barcelona, Spain."),
("Barcelona's hidden gems","past the tourist crowds","Barcelona Hidden Gems: Beyond the Tourist Trail","Past Las Ramblas and the crowds: the quiet Gracia squares, El Born wine bars, and the Bunkers del Carmel sunset that locals love. Barcelona's hidden gems for travelers who want more than the obvious, woven into a first-timer-friendly bucket list."),
("What not to miss in Barcelona","the experiences worth your time","Barcelona Bucket List: What Not to Miss (Honest Guide)","An honest take on Barcelona's must-dos: which experiences live up to the hype and which to skip. From Sagrada Familia and the Gothic Quarter to tapas crawls and beach afternoons, the Barcelona bucket list worth planning a trip around."),
("We came for Gaudi","we left obsessed with Barcelona","Why Barcelona Belongs on Your Bucket List","We came for Gaudi and left obsessed with the whole city: the tapas, the sunsets over the sea, the Gothic Quarter at night. The Barcelona experiences that turn a first visit into a lifelong love, all in one bucket list."),
("Only one day in Barcelona?","the can't-miss highlights, fast","Barcelona in One Day: The Must-See Highlights","Short on time in Barcelona? The can't-miss highlights, Sagrada Familia, the Gothic Quarter, La Boqueria and a sunset viewpoint, in one well-planned day. The fast-track Barcelona bucket list for first-timers."),
],
"4 Days in Barcelona":[
("The perfect 4 days in Barcelona","a first-timer's itinerary","4 Days in Barcelona: The Perfect First-Timer Itinerary","Gaudi, the Gothic Quarter, tapas and beach time: a 4-day Barcelona itinerary ordered so the city unfolds without backtracking. Day-by-day with Sagrada Familia and Park Guell timing, the best neighborhoods, where to eat, and where to stay. The complete first-timer plan for Barcelona, Spain."),
("Barcelona in 4 days","exactly what to do each day","4-Day Barcelona Itinerary: A Day-by-Day Plan","Four days in Barcelona mapped out: morning sights, afternoon neighborhoods, sunset spots, with the walking routes between. Sagrada Familia, Park Guell, the Gothic Quarter, the beach and the best tapas, in a logical day-by-day order for first-timers."),
("How to do the Gaudi sites right","in 4 perfect Barcelona days","4 Days in Barcelona: The Gaudi Highlights, Done Right","Sagrada Familia, Park Guell, Casa Batllo: which Gaudi sites are worth it, when to book, and how to fit them into 4 days without the lines. A first-timer's Barcelona itinerary built around the city's masterpieces."),
("First time in Barcelona?","your stress-free 4-day route","4 Days in Barcelona for First-Time Visitors","Where to stay, how to get around, and what to prioritize: a stress-free 4-day Barcelona itinerary for first-timers. The icons, the neighborhoods, and the tapas, in an order that actually flows."),
("Tapas, Gaudi, beach & sunsets","Barcelona in 4 unforgettable days","4 Days in Barcelona: The Perfect Mix","The perfect Barcelona mix in 4 days: Gaudi mornings, tapas afternoons, beach time and Bunkers del Carmel sunsets. A first-timer's day-by-day itinerary for Barcelona, Spain."),
("The Barcelona itinerary that just works","4 days, no wasted steps","4 Days in Barcelona: The Itinerary That Works","No backtracking, no wasted time: the 4-day Barcelona itinerary that just works. Sagrada Familia, the Gothic Quarter, Park Guell and the beach, mapped day by day for first-time visitors."),
("Barcelona's best sunset is worth the climb","and it fits perfectly into 4 days","4 Days in Barcelona: Sunsets, Sights & Tapas","Bunkers del Carmel at golden hour, the whole city to the sea: the Barcelona moments worth planning around, woven into a 4-day first-timer itinerary with Gaudi, tapas and the Gothic Quarter."),
],
"Where to Stay in Barcelona":[
("Where to stay in Barcelona","for first-time visitors","Where to Stay in Barcelona for First-Time Visitors","Not sure where to stay in Barcelona? The best neighborhoods compared, Eixample, the Gothic Quarter, El Born and Gracia, so you book the right area for your first trip, with honest pros and cons and where to avoid."),
("Don't book Barcelona","before reading this neighborhood guide","Where to Stay in Barcelona: The Neighborhood Guide","Before you book Barcelona, read this: the best neighborhoods for first-timers, where it's worth paying more, and the areas to skip. Eixample, Gothic Quarter, El Born and Gracia compared, so you don't book the wrong part of town."),
("Gothic Quarter or Eixample?","where to stay in Barcelona, sorted","Where to Stay in Barcelona: Gothic Quarter vs Eixample","The atmospheric Gothic Quarter or convenient Eixample? Barcelona's best neighborhoods compared for first-timers: what each trades off, and which fits your trip and budget."),
("The Barcelona neighborhood","you'll wish you'd booked","Best Areas to Stay in Barcelona","Village-like Gracia, central Eixample, lively El Born: the Barcelona neighborhood you'll wish you'd booked. The best areas to stay compared, with honest tips for first-time visitors."),
("Barcelona on a budget?","where to stay without overpaying","Where to Stay in Barcelona on a Budget","The smart Barcelona neighborhoods that keep you walkable to the sights without the price tag. Where to stay on a budget for a first trip: the best-value areas and what to expect."),
("Near the beach or the Gothic Quarter?","where to stay in Barcelona","Where to Stay in Barcelona: Beach vs City Center","Barceloneta sand or Gothic-Quarter buzz? How to choose your Barcelona base for the trip you want: the best neighborhoods for beach lovers, first-timers, and night owls."),
("We stayed in the wrong part first","here's where to book in Barcelona","Where to Stay in Barcelona (and Where Not To)","We learned the hard way, here's where to actually book in Barcelona and the area to avoid. The best neighborhoods for first-timers, compared honestly, so your stay is walkable and worth it."),
],
"Barcelona Travel Costs":[
("Is Barcelona expensive?","the honest answer, in real numbers","Barcelona Travel Costs: An Honest Budget Guide","Is Barcelona expensive? The honest answer in real numbers: hotels, tapas, Gaudi tickets and transit. What a Barcelona trip actually costs, with the swaps that bring it down. A realistic budget guide for first-timers."),
("What 4 days in Barcelona cost us","euro by euro","What 4 Days in Barcelona Actually Cost","A realistic Barcelona trip, line by line: flights, hotel, tapas, Gaudi tickets and transit. What 4 days in Barcelona actually cost us, euro by euro, plus where to spend less without missing the magic."),
("Barcelona on a budget?","it's cheaper than you think","Barcelona on a Budget: How to Visit for Less","Barcelona is cheaper than you think, if you know where to look. The big expenses and the smart swaps, from free Gaudi views to the menu del dia. How to do Barcelona, Spain on a budget."),
("Where to splurge, where to save","in Barcelona","Barcelona Travel Costs: Where to Splurge and Cut Back","The Barcelona experiences worth paying for and the ones to do free: a smarter way to budget your trip. Sagrada Familia tickets, tapas, hotels and transit, with honest splurge-or-skip calls."),
("Planning a Barcelona budget?","start with these real numbers","How Much Does a Barcelona Trip Cost?","Planning a Barcelona budget? Start with these real, current numbers: accommodation, food, attractions and transport per day. A realistic cost breakdown for a first trip to Barcelona, Spain."),
],
"Free Things to Do in Barcelona":[
("The best of Barcelona for free","and it doesn't feel cheap","Free Things to Do in Barcelona That Don't Feel Cheap","Bunker sunsets, beach afternoons, Gothic Quarter wandering and Gaudi from the outside: the best free things to do in Barcelona that still feel like the real thing. How to experience the city without spending."),
("Barcelona on zero euros?","here's how to do it","Free Things to Do in Barcelona","Beaches, viewpoints, markets and free museum hours: how to experience Barcelona on next to nothing. The best free things to do for budget-conscious first-timers, from the sea to the Bunkers del Carmel sunset."),
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
            r[h["Pin bold (vastag)"]] = b
            r[h["Pin light (vekony)"]] = l
            r[h["Pin cim"]] = t
            r[h["Pin leiras"]] = d
            cnt[a] = cnt.get(a, 0) + 1
with open(os.path.join(ROOT, "pins.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(rows[0]); w.writerows(rows[1:])
print("Updated per article:", cnt, "| total", sum(cnt.values()), "pins")
