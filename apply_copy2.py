# -*- coding: utf-8 -*-
"""Apply keyword-optimized copy for Rome + Amalfi + Dolomites clusters."""
import csv, os

COPY = {
"3 Days in Rome Itinerary (VERIFY SLUG)":[
("The perfect 3 days in Rome","a first-timer's itinerary","3 Days in Rome Itinerary: The Perfect First-Timer Route","The Colosseum, the Vatican, the Pantheon and Trastevere: a 3-day Rome itinerary ordered so you walk less and see more. Day-by-day with skip-the-line tips, where to stay, and what 3 days in Rome really costs. Your complete first-timer guide to the Eternal City."),
("First time in Rome?","your no-stress 3-day route","3 Days in Rome for First-Time Visitors","Where to stay, what to book ahead, and the walking route that ties it together: a stress-free 3-day Rome itinerary for first-timers. The Colosseum, Roman Forum, Trevi Fountain and Trastevere, in an order that flows."),
("The most beautiful corners of Rome","mapped into 3 perfect days","3 Days in Rome: The Most Beautiful Route","From the Pantheon's open dome to the Trevi Fountain and Trastevere's lanes: the most beautiful corners of Rome, mapped into 3 perfect days. A first-timer's itinerary built around the city's prettiest spots."),
("Rome in 3 days, no chaos","exactly what to do each day","3-Day Rome Itinerary: A Day-by-Day Plan","Three days in Rome mapped hour by hour: what to see, when to go, and where to eat between the Colosseum, Vatican, Pantheon and Trevi Fountain. The day-by-day plan that keeps a first Rome trip calm, not chaotic."),
("The Colosseum at opening hits different","start your 3 days in Rome here","3 Days in Rome: Beat the Crowds at the Big Sights","The Colosseum and Vatican empty out at the right hour: a 3-day Rome itinerary timed around the quiet windows most visitors miss, plus Trastevere, the Pantheon and the Trevi Fountain after dark."),
("Trastevere at golden hour","the Rome most first-timers miss","3 Days in Rome: Don't Skip Trastevere","Cobbled lanes, ivy, dinners that last for hours: why Trastevere belongs in every 3-day Rome itinerary, plus the Colosseum, Vatican and Pantheon, in a first-timer route that walks beautifully."),
("Rome on foot in 3 days","the walkable first-timer route","3 Days in Rome: A Walkable Itinerary","Rome rewards walking. A 3-day itinerary that connects the Colosseum, Pantheon, Trevi Fountain and Trastevere on foot, with the gelato stops to match. The first-timer route that flows."),
("3 days in Rome, done right","what to book, see and skip","3 Days in Rome: What to Book, See and Skip","Honest about what's worth booking ahead (Colosseum, Vatican), what's worth your time, and what to skip: the 3-day Rome itinerary that makes a first trip click. Day by day, with real costs."),
("What I'd do differently in Rome","a smarter 3-day itinerary","3 Days in Rome: What I'd Change on a Second Visit","The timing mistakes, the sights worth more time, and the one I'd skip: a smarter 3-day Rome itinerary for first-timers, built from lessons learned. Colosseum, Vatican, Pantheon and Trastevere, done right."),
],
"Best Things to Do in Rome (NEW)":[
("The most beautiful places in Rome","and how to see them in one trip","The Most Beautiful Places in Rome (First-Timer's Guide)","From the Pantheon and Trevi Fountain to Trastevere's lanes and the Roman Forum: the most beautiful places in Rome and how to see them in one trip. The best things to do for a first visit to the Eternal City."),
("Best things to do in Rome","ranked honestly for first-timers","Best Things to Do in Rome: An Honest First-Timer List","Ancient icons, piazzas and the experiences that earn the hype: the best things to do in Rome, ranked honestly for first-timers. From the Colosseum and Vatican to the food and the free spots, with what's worth it and what to skip."),
("Rome's hidden gems","beyond the Colosseum and Trevi","Rome Hidden Gems: Beyond the Tourist Trail","Quiet churches, local trattorias, the Aventine keyhole and Monti's lanes: Rome's hidden gems for travelers who want more than the obvious. The best things to do past the Colosseum and Trevi Fountain."),
("The most Instagrammable spots in Rome","and when to shoot them","Most Instagrammable Spots in Rome (+ Best Times)","The Colosseum at dawn, the Trevi Fountain after dark, the Aventine keyhole and the Spanish Steps: the most photogenic spots in Rome and when to shoot them, crowd-free. A first-timer's photo guide."),
("First time in Rome?","start with these must-dos","Best Things to Do in Rome for First-Time Visitors","The Rome must-dos that make a first trip click: the Colosseum, Vatican, Pantheon and Trastevere, plus the food and the moments to plan around. The best things to do for first-timers."),
("The Rome moment that gives you chills","and where to find it","Best Things to Do in Rome: The Unmissable Moments","The Pantheon's open dome, the Forum at golden hour, the Trevi at midnight: the Rome experiences that stay with you. The best things to do for a first, unforgettable trip."),
("Eat your way through Rome","the food worth traveling for","Best Things to Do in Rome: The Food Worth Traveling For","Cacio e pepe, the perfect espresso, gelato worth the walk and Trastevere trattorias: eating your way through the best of Rome. A first-timer's food guide to the Eternal City."),
("Worth it or overrated in Rome?","an honest first-timer take","Best Things to Do in Rome: Worth It or Overrated?","An honest take on Rome's biggest attractions: which ones earn your time (Colosseum, Pantheon) and which you can happily skip. The best things to do, ranked for first-time visitors."),
],
"Where to Stay in Rome (NEW)":[
("Where to stay in Rome","for first-time visitors","Where to Stay in Rome for First-Time Visitors","Not sure where to stay in Rome? Monti, Centro Storico and Trastevere compared, so you book the right area for your first trip. Walkable to the Colosseum, Pantheon and Trevi, with honest pros and cons."),
("The Rome neighborhood with the most charm","and where to book it","Where to Stay in Rome: Trastevere & the Best Areas","Cobbled lanes and great dinners minutes from the sights: why Trastevere and Monti are the Rome neighborhoods first-timers love. Where to stay, compared honestly, with where to avoid."),
("Don't book Rome","before reading this neighborhood guide","Where to Stay in Rome: The Neighborhood Guide","Before you book Rome, read this: Monti for charm and value, Centro Storico for convenience, Trastevere for evenings. The best neighborhoods for first-timers, plus the area to skip near Termini."),
("Rome on a budget?","where to stay without overpaying","Where to Stay in Rome on a Budget","Central-enough Rome neighborhoods that save money and keep you walking to the Colosseum and Pantheon. Where to stay on a budget for a first trip, with the best-value areas and what to expect."),
],
"Rome Travel Costs (NEW)":[
("Is Rome expensive?","the honest answer, in real numbers","Rome Travel Costs: An Honest Budget Guide","Is Rome expensive? The honest answer in real numbers: hotels, food, Colosseum and Vatican tickets, transit. What a Rome trip actually costs, with the swaps that cut the bill. A realistic budget guide for first-timers."),
("What 3 days in Rome cost","euro by euro","What 3 Days in Rome Actually Cost","A realistic Rome trip, line by line: hotel, food, Colosseum and Vatican tickets, transit. What 3 days in Rome actually cost, euro by euro, plus where to save without missing the magic."),
("Can you do Rome on a budget?","yes, here's the real daily cost","Rome on a Budget: How to Visit for Less","Yes, you can do Rome on a budget. The big expenses and the smart ways around them, from free piazzas and viewpoints to the trattorias locals use. How to see the Eternal City for less."),
],
"Free Things to Do in Rome (NEW)":[
("The best free things to do in Rome","that still wow","Free Things to Do in Rome That Still Wow","The Pantheon, the piazzas, the Trevi Fountain and the best free views: the best free things to do in Rome that still feel like the real thing. How to experience the Eternal City without spending."),
("Rome without spending a euro","the best free spots","Free Things to Do in Rome","Fountains, churches, the Spanish Steps and golden-hour viewpoints: how to experience Rome for free. The best free things to do for budget-conscious first-timers in the Eternal City."),
],
"Day Trips from Rome (NEW)":[
("The best day trips from Rome","beyond the city","Best Day Trips from Rome: Where to Go","Tivoli's gardens, Ostia's ruins, hill towns and the coast: the best day trips from Rome, ranked by what's worth it. How to escape the city for a day, with the easiest ways to get there."),
],
"Best Time to Visit Rome (NEW)":[
("When to visit Rome (and when not to)","season by season","Best Time to Visit Rome: Season by Season","Mild shoulder months, hot crowded summers, quiet winters: the best time to visit Rome, season by season, with honest crowd and weather notes. When to go for the trip you want, first-timer-friendly."),
],
"Amalfi Coast 5-Day Itinerary":[
("The perfect 5 days on the Amalfi Coast","a first-timer's itinerary","5 Days on the Amalfi Coast: The Perfect Itinerary","Positano, Amalfi, Ravello and the villages between: a 5-day Amalfi Coast itinerary that gives each town the time it deserves. Day-by-day with ferries, the Path of the Gods, where to base, and how to do the coast without a car."),
("Amalfi Coast in 5 days","exactly what to do each day","5-Day Amalfi Coast Itinerary: A Day-by-Day Plan","Five days on the Amalfi Coast mapped out: Positano, Ravello, a Capri day and the Path of the Gods, with ferry timing between. The day-by-day itinerary that makes a first trip flow."),
("The Amalfi day worth spending on the water","Capri & the coast by boat","5 Days on the Amalfi Coast: The Ferry & Capri Day","The coast looks completely different from the water. How to fit Capri, the Blue Grotto and a ferry day into a 5-day Amalfi Coast itinerary, with Positano and Ravello on land."),
("Ravello: the Amalfi town people skip","and regret missing","5-Day Amalfi Coast Itinerary: Why Ravello Deserves a Day","Gardens above the sea, fewer crowds, the best view on the whole coast: why Ravello earns a full day on a 5-day Amalfi itinerary, alongside Positano, Amalfi and a Capri day trip."),
("The Path of the Gods is worth the climb","and it fits into 5 days","5 Days on the Amalfi Coast: The Path of the Gods","One morning on the Path of the Gods and the coast looks different from above. Where the famous hike fits in a 5-day Amalfi itinerary, with Positano, Ravello and ferry days."),
("First time on the Amalfi Coast?","read this before you book","5 Days on the Amalfi Coast for First-Timers","Where to base, how the ferries work, and which towns to prioritize: the 5-day Amalfi Coast itinerary I wish I'd had on my first visit. Positano, Amalfi, Ravello and Capri, done right."),
("The Amalfi Coast at its most unreal","Positano, Ravello & the sea","5 Days on the Amalfi Coast: The Most Beautiful Stops","Cliffside villages, turquoise coves and lemon terraces over the sea: the most beautiful stops on the Amalfi Coast, mapped into 5 perfect days. One of the most beautiful places in Italy."),
],
"Amalfi Coast Bucket List":[
("The most beautiful places on the Amalfi Coast","and how to see them","Amalfi Coast Bucket List: The Most Beautiful Stops","Positano tumbling to the sea, Ravello's gardens, coves you reach by boat: the most beautiful places on the Amalfi Coast and how to see them. The bucket list for one of the most beautiful places in Italy."),
("Amalfi by boat: the bucket-list day","Capri, coves & the Blue Grotto","Amalfi Coast Bucket List: The Best Things to Do by Sea","The coast looks completely different from the water: the boat days, hidden coves and swims that top an Amalfi bucket list, plus Capri and the Blue Grotto. The experiences worth planning a trip around."),
("The Amalfi lemon experience","limoncello, granita & long lunches","Amalfi Coast Bucket List: Lemons, Limoncello & Long Lunches","Terraced lemon groves, granita in the shade, the long Amalfi lunch: the flavors that belong on an Amalfi Coast bucket list, alongside Positano, Ravello and the sea."),
("The Amalfi beach worth the climb down","hidden coves & swims","Amalfi Coast Bucket List: The Best Beaches & Coves","Fornillo, Furore, the coves only boats reach: the Amalfi Coast swims worth the stairs and the detour. The bucket-list beaches for one of the most beautiful coastlines in Italy."),
("First time on the Amalfi Coast?","the experiences worth every euro","Amalfi Coast Bucket List for First-Timers","What's genuinely worth it on a first Amalfi trip: Positano, Ravello, the Path of the Gods, a Capri day and the food. The bucket list ranked honestly for first-time visitors."),
("The Amalfi sunset you'll never forget","Positano & Ravello at golden hour","Amalfi Coast Bucket List: The Best Sunsets","Positano glowing gold, Ravello above the clouds: the Amalfi Coast sunsets worth building an evening around. The bucket-list moments for one of Italy's most beautiful places."),
("Amalfi Coast bucket list","25 experiences worth the trip","Amalfi Coast Bucket List: 25 Unmissable Experiences","Beyond the photos: the Amalfi experiences, towns and meals worth planning a trip around, from Positano and Ravello to the Path of the Gods and a Capri day. Ranked by what's truly worth it."),
],
"Where to Stay on the Amalfi Coast":[
("Where to stay on the Amalfi Coast","for first-time visitors","Where to Stay on the Amalfi Coast for First-Timers","Positano, Amalfi, Praiano or Sorrento? The best Amalfi Coast towns compared, so you book the right base for your first trip. Close to the ferries, the views and the towns you came for."),
("Positano or Praiano?","where to stay on the Amalfi Coast","Where to Stay on the Amalfi Coast: Positano vs Praiano","The glamour of Positano or the value and calm of Praiano? How to choose your Amalfi base and what each trades off. The best towns to stay compared for first-timers."),
("The Amalfi base that costs you less","without missing the views","Where to Stay on the Amalfi Coast on a Budget","Smart towns that put you on the coast without Positano prices: where to base an Amalfi trip and still spend less. Praiano, Atrani, Maiori and more, compared honestly."),
("The Amalfi hotel with the view","rooms over the sea","Where to Stay on the Amalfi Coast: Rooms with a Sea View","Waking to the coast from your terrace: the Amalfi towns and stays where the sea view is the whole point. Where to book for Positano and Ravello views, first-timer-friendly."),
("No car on the Amalfi Coast?","stay in these towns","Where to Stay on the Amalfi Coast Without a Car","Ferry-linked, walkable bases where you don't need to drive the cliff road: the easiest Amalfi towns to stay in. Positano, Amalfi and Sorrento compared for car-free first-timers."),
("The quiet Amalfi town to base in","past the Positano crowds","Where to Stay on the Amalfi Coast: The Calmer Towns","Past the crowds of Positano: the Amalfi towns that stay calm, like Ravello, Atrani and Praiano. Where to base for a slower, quieter coast, with honest tips."),
("Don't book the Amalfi Coast","before reading this town guide","Where to Stay on the Amalfi Coast: The Town Guide","Before you book the Amalfi Coast, read this: which town suits your trip, where it's worth paying more, and how to avoid the cliff-road hassle. Positano, Amalfi, Ravello and Praiano compared."),
],
"Amalfi Coast Travel Costs":[
("Is the Amalfi Coast expensive?","the honest answer","Amalfi Coast Travel Costs: An Honest Budget Guide","Is the Amalfi Coast worth the price? The honest answer in real numbers: hotels, ferries, restaurants and beach clubs. What an Amalfi trip actually costs, and how to spend less."),
("What 5 days on the Amalfi Coast cost","euro by euro","What 5 Days on the Amalfi Coast Actually Cost","A realistic Amalfi trip, line by line: hotel, ferries, Positano lunches and a Capri day. What 5 days on the Amalfi Coast actually cost, euro by euro, plus the swaps that make it cheaper."),
("Amalfi Coast on a budget?","the real tips that work","Amalfi Coast on a Budget: How to Do It for Less","The base, the ferries and the meals that cost less: how to enjoy the Amalfi Coast without overspending. From Praiano stays to picnic swims, a budget guide for first-timers."),
("Where to splurge, where to save","on the Amalfi Coast","Amalfi Coast Travel Costs: Where to Splurge & Cut Back","The Amalfi experiences worth the money (a boat day, a Ravello terrace) and the ones to skip: a smarter way to budget the coast. Hotels, ferries and food, with honest splurge-or-save calls."),
],
"Free Things to Do on the Amalfi Coast":[
("The Amalfi Coast for free","cliff walks & hidden beaches","Free Things to Do on the Amalfi Coast","Cliffside walks, public beaches and the Path of the Gods: the best of the Amalfi Coast that costs nothing. How to enjoy Positano, Amalfi and Ravello between the pricier days."),
("Amalfi without spending a euro","views, walks & swims","Free Things to Do on the Amalfi Coast That Still Wow","Free coastal trails, village wandering and cove swims: how to enjoy the Amalfi Coast on next to nothing. The best free things to do for budget-conscious first-timers."),
],
"14-Day Southern Italy Road Trip":[
("Southern Italy in 14 days, by car","Amalfi, Naples & Puglia","14-Day Southern Italy Road Trip Itinerary","Naples, the Amalfi Coast, Puglia and the deep south: a 14-day southern Italy road trip linking the coast, the food and the hill towns. The full driving route, where to stay, and what not to miss."),
],
"Hiking in the Dolomites":[
("The 5 best hikes in the Dolomites","you have to do","Best Hiking Trails in the Dolomites You Must Do","From Tre Cime di Lavaredo to Seceda and Cadini di Misurina: the best hiking trails in the Italian Dolomites, sorted by difficulty so you can match the trail to your fitness and the view payoff."),
("Lago di Braies & the Dolomites' best trails","for every level","Hiking in the Dolomites: Best Trails for Every Level","From easy Lago di Braies loops to the dramatic Tre Cime circuit: the best Dolomites hikes for every level, with what to pack, the best time to go, and honest notes on crowds and gondola access."),
("The Dolomites hike worth a 5am alarm","Tre Cime at sunrise","Best Sunrise Hikes in the Dolomites","First light on Tre Cime di Lavaredo and the whole valley turns pink: the Dolomites trails worth the early start, like Cadini di Misurina and Seceda, with the timing that makes it work."),
("Lakes so blue they look edited","the best Dolomites lake hikes","Dolomites Lake Hikes: Lago di Braies & Beyond","Lago di Braies, Sorapis and the quieter lakes most visitors miss: the Dolomites hikes that end at impossibly turquoise water. The most beautiful lake trails in the Italian Alps."),
("Seceda: the Dolomites view that stops you cold","and how to hike it","Hiking the Dolomites: Seceda & the Best Views","The jagged Seceda ridge, the Odle peaks, Alpe di Siusi meadows: the Dolomites viewpoints that make you stop and stare, and the trails that lead to them. Mapped by effort and reward."),
("Hut to hut in the Dolomites","what it's really like","Hut-to-Hut Hiking in the Dolomites: How It Works","Sleeping in a mountain rifugio, hot meals at 8,000 feet, waking up above the clouds: how multi-day Dolomites hiking actually works for first-timers, with the best hut-to-hut routes."),
("Hiking the Dolomites with kids","trails that actually work","Family Hikes in the Dolomites: Easy Trails with Big Views","Gondola-assisted trails, meadow walks and rifugio lunches: the Dolomites hikes that keep little legs happy and still feel like a real adventure, from Alpe di Siusi to Lago di Braies."),
("The Dolomites without a car","trails you can reach easily","Hiking in the Dolomites Without a Car","Lift-linked trails that start at your door: how to hike the best of the Dolomites (Seceda, Tre Cime, Lago di Braies) without renting a car. The car-free guide for first-timers."),
("Trail runners or boots in the Dolomites?","what you actually need","Hiking in the Dolomites: Trails, Timing & What to Pack","The trails worth your days (Tre Cime, Seceda, Cadini di Misurina), when to go, and the gear that actually matters in the Italian Alps. The practical hiking guide I wish I'd had on trip one."),
],
"Where to Stay in the Dolomites":[
("Where to stay in the Dolomites","best areas for first-timers","Where to Stay in the Dolomites: Best Areas for First-Timers","Cortina, Val Gardena or Alta Badia? The best Dolomites bases compared, so you pick the valley that fits your hikes and your pace. Close to Tre Cime, Seceda and Lago di Braies."),
("The Dolomites base you don't need a car for","stay here","Where to Stay in the Dolomites Without a Car","Lift-linked villages where the trails start at your door: the Dolomites bases that work without renting a car. Val Gardena, Ortisei and more, compared for car-free first-timers."),
("Val Gardena or Alta Badia?","where to stay in the Dolomites","Where to Stay in the Dolomites: Val Gardena vs Alta Badia","Two of the best Dolomites valleys compared: scenery, access to Seceda and the trails, and which suits your kind of mountain trip. Where to base for first-timers."),
("The Dolomites hotel with the view","rooms facing the peaks","Where to Stay in the Dolomites: Rooms with Mountain Views","Waking up to the peaks from your window: the Dolomites areas and stays where the view is the whole point, near Seceda, Tre Cime and Alpe di Siusi."),
("The Dolomites on a budget","where to stay for less","Where to Stay in the Dolomites on a Budget","Family-run guesthouses and half-board deals: where to stay in the Dolomites without paying Cortina prices. The best-value valleys and towns for first-timers."),
("The Dolomites with kids","best areas for families","Where to Stay in the Dolomites for Families","Gentle trails, gondolas and playgrounds with a view: the Dolomites bases that work best with kids, from Val Gardena to Alpe di Siusi. Where to stay for a family trip."),
("Cortina or a quieter valley?","where to stay in the Dolomites","Where to Stay in the Dolomites: Cortina vs the Quiet Valleys","The glamour of Cortina or the calm of a smaller village: how to choose your Dolomites base and what each trades off. The best areas for first-timers, with honest tips."),
],
"Dolomites Day Trip from Venice":[
("Venice to the Dolomites in a day","how to do it","Dolomites Day Trip from Venice: How to Do It","Trading canals for peaks in a single day: how to see the Dolomites from Venice, whether to drive or tour, and the stops worth it, like Lago di Braies and Cortina."),
("Is a Dolomites day trip from Venice worth it?","the honest answer","Dolomites Day Trip from Venice: Is It Worth It?","Three hours each way for the mountains of your life: an honest take on the Dolomites day trip from Venice, what you'll actually see, and whether to do it."),
("The lake that makes the Venice day trip","Lago di Braies & more","Dolomites Day Trip from Venice: Lago di Braies & Cortina","Lago di Braies, Cortina and a peak or two: the Dolomites day trip from Venice worth the early start. What to see and how to fit it into one day."),
("Venice to the mountains: the smart route","what to see in one day","Dolomites Day Trip from Venice: The Best Route","Where to go and what to skip when you only have a day: the Dolomites day trip from Venice, planned well, with Lago di Braies and the best viewpoints."),
("Dolomites in a day: tour or drive?","how to choose","Dolomites Day Trip from Venice: Tour vs Self-Drive","Guided ease or your own car and pace: how to choose for a Dolomites day trip from Venice. The pros, cons and the route either way."),
("The alpine escape from Venice","turquoise lakes & jagged peaks","Dolomites Day Trip from Venice: A Mountain Day Out","Turquoise lakes and jagged peaks a few hours from the lagoon: the Dolomites day trip that surprises Venice visitors. Lago di Braies, Cortina and the best stops."),
("One day, Venice to the Dolomites","a first-timer's plan","Dolomites Day Trip from Venice for First-Timers","The timing, the stops and the views worth the drive: a first Dolomites day trip from Venice made simple, with Lago di Braies and the most beautiful spots."),
],
"Best Time to Visit the Dolomites":[
("When the Dolomites look their best","month by month","Best Time to Visit the Dolomites: Month by Month","Wildflower summers, golden larch autumns, snow-quiet winters: when to visit the Dolomites for the trip you want, with honest crowd and weather notes for Seceda, Tre Cime and the lakes."),
("The best month for the Dolomites","the sweet spot","Best Time to Visit the Dolomites: The Sweet Spot","The window with open trails, good weather and fewer crowds: the best month to visit the Dolomites, explained, so your hikes to Tre Cime and Lago di Braies land just right."),
("The Dolomites in autumn gold","when the larches turn","Best Time to Visit the Dolomites: Autumn Magic","When the larch forests turn gold and the crowds thin: why autumn might be the best time in the Dolomites, with the best spots to see the colour around Seceda and the lakes."),
("How to skip the Dolomites crowds","when to go","Best Time to Visit the Dolomites: When to Avoid the Crowds","The weeks with the views but not the queues: when to visit the Dolomites for quiet trails and clear roads, from Tre Cime to Lago di Braies. Timing tips for first-timers."),
],
"Milan to Dolomites Road Trip":[
("Milan to the Dolomites: the scenic drive","the route & best stops","Milan to Dolomites Road Trip: The Best Route","Lakes, vineyards and the first sight of the peaks: the Milan to Dolomites road trip, mapped with the stops worth making, from Lake Garda to Seceda and Lago di Braies."),
],
"Dolomites from Milan":[
("Milan to the Dolomites: how to do it","the route & drive time","How to Get to the Dolomites from Milan","The route, the drive time and the first stops: how to reach the Dolomites from Milan and make the most of it, with Lago di Braies, Cortina and the best viewpoints."),
],
"24 Hours in Milan":[
("Milan in 24 hours","the perfect one-day plan","24 Hours in Milan: A Perfect One-Day Itinerary","The Duomo, the Last Supper and an aperitivo at golden hour: how to make the most of 24 hours in Milan, with a walkable one-day route for first-timers."),
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
