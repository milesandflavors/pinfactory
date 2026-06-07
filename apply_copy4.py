# -*- coding: utf-8 -*-
"""Apply keyword-optimized copy for Japan + Chicago clusters."""
import csv, os

COPY = {
"Japan 10-Day Itinerary":[
("The perfect 10 days in Japan","Tokyo, Kyoto & beyond","Japan 10-Day Itinerary: Tokyo, Kyoto & Osaka","Tokyo's neon, Kyoto's temples, Osaka's food and a Mt Fuji view: a 10-day Japan itinerary that hits the icons without rushing. Day-by-day with bullet trains, where to stay, and what to book. The first-timer route."),
("First time in Japan?","this 10-day route nails it","Japan 10-Day Itinerary for First-Timers","Where to go, how the bullet trains work, and what to prioritize: the 10-day Japan itinerary I wish I'd had. Tokyo, Kyoto, Osaka and Hakone, in an order that flows for first-timers."),
("Tokyo to Kyoto in 10 days","the can't-miss route","10 Days in Japan: Tokyo to Kyoto, Done Right","Shibuya, Senso-ji, Fushimi Inari, the Arashiyama bamboo and a Fuji day: the 10-day Japan route that connects the icons by bullet train. Where to stay and what not to miss."),
("Japan in 10 days, no rush","the itinerary that works","Japan 10-Day Itinerary: The Route That Works","Neon nights, ancient temples, the best food on earth: a 10-day Japan itinerary balanced so you see Tokyo, Kyoto and Osaka without burning out. Mapped day by day for first-timers."),
],
"Best Things to Do in Tokyo":[
("The best things to do in Tokyo","for first-timers","Best Things to Do in Tokyo for First-Timers","Shibuya Crossing, Senso-ji, teamLab and the best ramen: the best things to do in Tokyo, ranked for first-timers. What's worth it, what to skip, and how to fit it in."),
("Tokyo hidden gems","beyond Shibuya & Shinjuku","Tokyo Hidden Gems: Beyond the Big Sights","Yanaka's old streets, hidden izakaya alleys, quiet shrines and the best local eats: Tokyo's hidden gems for travelers who want more than Shibuya. The best things to do off the tourist trail."),
("The most beautiful spots in Tokyo","and when to go","Most Beautiful Places in Tokyo (+ Best Times)","Senso-ji at dawn, the Shibuya lights, cherry blossoms by the river and skyline views: the most beautiful places in Tokyo and when to see them. A first-timer's guide."),
("Eat your way through Tokyo","the food worth the flight","Best Things to Do in Tokyo: The Food Worth the Flight","Ramen, sushi, the best convenience-store snacks and izakaya nights: eating your way through Tokyo. A first-timer's food guide to the best bites in the city."),
],
"Best Things to Do in Osaka":[
("The best things to do in Osaka","Japan's food capital","Best Things to Do in Osaka for First-Timers","Dotonbori's neon, Osaka Castle, street food and day trips to Nara: the best things to do in Osaka, ranked for first-timers. What's worth it and how to fit it in."),
("Eat your way through Osaka","takoyaki, okonomiyaki & more","Best Things to Do in Osaka: The Food Guide","Takoyaki, okonomiyaki, kushikatsu and the buzz of Dotonbori: eating your way through Osaka, Japan's food capital. A first-timer's guide to the best bites."),
("Osaka in a day or two","the can't-miss spots","Best Things to Do in Osaka: The Highlights","Osaka Castle, Dotonbori, Shinsekai and a Nara day trip: the can't-miss things to do in Osaka, mapped for a short stay. The first-timer highlights."),
("Osaka after dark","neon, food & nightlife","Best Things to Do in Osaka at Night","Dotonbori's glowing canal, street-food stalls and the city's nightlife: the best things to do in Osaka after dark. A first-timer's evening guide."),
],
"Hakone Day Trip from Tokyo":[
("The perfect Hakone day trip","Mt Fuji, onsen & Lake Ashi","Hakone Day Trip from Tokyo: The Perfect Plan","Mt Fuji views, an onsen soak, the Lake Ashi pirate ship and the ropeway: how to do Hakone as a day trip from Tokyo, step by step. The route, the pass, and the best stops."),
("See Mt Fuji from Tokyo in a day","here's how","Hakone Day Trip from Tokyo: How to See Mt Fuji","The easiest way to see Mt Fuji from Tokyo: a Hakone day trip with the ropeway, Lake Ashi and an onsen. How to do it, what to book, and the best Fuji viewpoints."),
("Is a Hakone day trip worth it?","the honest answer","Hakone Day Trip from Tokyo: Is It Worth It?","Mt Fuji, hot springs and lake views an hour from Tokyo: an honest take on the Hakone day trip, what you'll see, and whether to stay overnight instead."),
("Tokyo to Hakone made easy","the loop, the pass & the views","Hakone Day Trip from Tokyo: The Easy Loop","The famous Hakone loop, train, ropeway, boat and bus, made simple: how to see Mt Fuji, Lake Ashi and the onsen in one day from Tokyo, with the pass that saves money."),
],
"Best Things to Do in Kyoto":[
("The best things to do in Kyoto","temples, geisha & bamboo","Best Things to Do in Kyoto for First-Timers","Fushimi Inari's torii gates, the Arashiyama bamboo grove, Kinkaku-ji and Gion: the best things to do in Kyoto, ranked for first-timers. What's worth it and how to fit it in."),
("The most beautiful spots in Kyoto","and when to go","Most Beautiful Places in Kyoto (+ Best Times)","Fushimi Inari at dawn, the bamboo grove before the crowds, golden Kinkaku-ji: the most beautiful places in Kyoto and when to see them. A first-timer's photo guide."),
("Kyoto's temples & torii gates","the can't-miss sights","Best Things to Do in Kyoto: Temples & Torii","Fushimi Inari, Kinkaku-ji, Kiyomizu-dera and the geisha streets of Gion: the can't-miss sights in Kyoto, mapped to skip the crowds. A first-timer's guide."),
],
"Where to Stay in Tokyo":[
("Where to stay in Tokyo","best areas for first-timers","Where to Stay in Tokyo for First-Time Visitors","Shinjuku, Shibuya, Ginza or Asakusa? The best Tokyo neighborhoods compared, so you book the right base for your first trip. Close to the trains, the sights and the food."),
("Shinjuku or Shibuya?","where to stay in Tokyo","Where to Stay in Tokyo: Shinjuku vs Shibuya","Two of Tokyo's best bases compared: nightlife, transport links and what each is like to stay in. Where to base your first Tokyo trip, with honest tips."),
("Tokyo on a budget?","where to stay for less","Where to Stay in Tokyo on a Budget","Smart Tokyo neighborhoods near the trains without the high price tag: where to stay on a budget for a first trip. The best-value areas and what to expect."),
],
"Japan Travel Costs":[
("Is Japan expensive?","the honest answer","Japan Travel Costs: An Honest Budget Guide","Is Japan expensive? The honest answer in real numbers: hotels, food, the JR Pass and attractions. What a Japan trip actually costs, with the swaps that bring it down. A realistic budget guide."),
],
"Best Time to Visit Japan":[
("When to visit Japan","cherry blossoms, fall & beyond","Best Time to Visit Japan: Season by Season","Cherry blossoms in spring, fiery maples in fall, quiet winters: the best time to visit Japan, season by season, with honest crowd and weather notes. When to go for the trip you want."),
],
"Japan Cherry Blossom Season":[
("When & where to see cherry blossoms in Japan","the timing guide","Japan Cherry Blossom Season: When & Where to Go","When the cherry blossoms peak and the best places to see them, from Kyoto's temples to Tokyo's rivers. How to time a Japan trip around sakura season, for first-timers."),
("Chasing cherry blossoms in Japan","the best spots & timing","Cherry Blossom Season in Japan: Best Spots","Kyoto's Philosopher's Path, Tokyo's Meguro River, castle moats lined in pink: the best places to see cherry blossoms in Japan and exactly when to go. A first-timer's sakura guide."),
],
"Ryokan in Japan What to Expect":[
("Staying in a ryokan in Japan","what to expect","Staying in a Ryokan in Japan: What to Expect","Tatami floors, onsen baths, kaiseki dinners and futon beds: what to expect at a traditional Japanese ryokan, plus how to choose one and the etiquette to know. A first-timer's guide."),
],
"Chicago Bucket List":[
("The Chicago bucket list","for first-timers","Chicago Bucket List: 25 Best Things to Do","The Bean, the architecture cruise, deep dish and the skyline views: the Chicago bucket list worth your time, ranked honestly for first-timers. What's worth it and what to skip."),
("The most beautiful spots in Chicago","and how to see them","Most Beautiful Places in Chicago","Cloud Gate's mirror, the river at golden hour, the lakefront skyline and Millennium Park: the most beautiful places in Chicago and how to see them. A first-timer's guide."),
("Chicago hidden gems","beyond the Bean","Chicago Hidden Gems: Beyond the Tourist Spots","Hidden speakeasies, lakefront neighborhoods, local eats and quiet viewpoints: Chicago's hidden gems for travelers who want more than the Bean. The best things to do off the beaten path."),
("The best Chicago views","skyline, river & lake","Chicago Bucket List: The Best Skyline Views","The Skydeck ledge, 360 Chicago, the river at dusk and the lakefront: the best Chicago skyline views and when to go. The can't-miss viewpoints for a first trip."),
("First time in Chicago?","start with these must-dos","Best Things to Do in Chicago for First-Timers","The Bean, the architecture river cruise, deep dish and the lakefront: the Chicago must-dos that make a first trip click. The best things to do, ranked for first-time visitors."),
("Eat your way through Chicago","deep dish & beyond","Chicago Bucket List: The Food Worth Traveling For","Deep dish, Italian beef, the best food halls and lakefront patios: eating your way through Chicago. A first-timer's food guide to the city's best bites."),
("The Chicago architecture cruise","worth every minute","Chicago Bucket List: The Architecture River Cruise","Gliding past skyscrapers with the story behind each: why the architecture river cruise tops a Chicago bucket list, plus the Bean, the Skydeck and the lakefront."),
],
"3 Days in Chicago":[
("The perfect 3 days in Chicago","a first-timer's itinerary","3 Days in Chicago: The Perfect Itinerary","The Bean, the architecture cruise, deep dish and the lakefront: a 3-day Chicago itinerary ordered so you see the best without rushing. Day-by-day with where to stay and what to book."),
("Chicago in 3 days","exactly what to do each day","3-Day Chicago Itinerary: A Day-by-Day Plan","Three days in Chicago mapped out: Millennium Park, the river cruise, the Art Institute, the Skydeck and the lakefront. The day-by-day itinerary for first-time visitors."),
("First time in Chicago?","your no-stress 3-day route","3 Days in Chicago for First-Time Visitors","Where to stay, how to get around, and what to prioritize: a stress-free 3-day Chicago itinerary. The Bean, the architecture cruise and deep dish, in an order that flows."),
("Chicago in 3 days, done right","what to see, eat & skip","3 Days in Chicago: What to See, Eat and Skip","Honest about what's worth it: the Bean, the river cruise and the Skydeck, plus the deep dish worth the wait. The 3-day Chicago itinerary that makes a first trip click."),
("The best of Chicago in a weekend","3 perfect days","3 Days in Chicago: The Perfect Weekend","A weekend that hits the icons: Millennium Park, the architecture cruise, the lakefront and the best food. The 3-day Chicago itinerary for first-timers."),
("Chicago's skyline, river & lake","in 3 unforgettable days","3 Days in Chicago: Skyline, River & Lake","The Skydeck ledge, the river at golden hour, the lakefront path: the Chicago moments worth planning around, woven into a 3-day first-timer itinerary."),
("Chicago on foot in 3 days","the walkable route","3 Days in Chicago: A Walkable Itinerary","Chicago's best is walkable: a 3-day itinerary linking Millennium Park, the Riverwalk, the Art Institute and the lakefront on foot, with deep-dish stops to match."),
],
"Where to Stay in Chicago":[
("Where to stay in Chicago","for first-time visitors","Where to Stay in Chicago for First-Time Visitors","The Loop, River North, the Gold Coast or Wicker Park? The best Chicago neighborhoods compared, so you book the right area for your first trip. Honest pros, cons and what to avoid."),
("The Loop or River North?","where to stay in Chicago","Where to Stay in Chicago: The Loop vs River North","Central sightseeing or nightlife and dining? How to choose your Chicago base and what each trades off. The best neighborhoods to stay, compared for first-timers."),
("Don't book Chicago","before reading this neighborhood guide","Where to Stay in Chicago: The Neighborhood Guide","Before you book Chicago, read this: which neighborhood suits your trip, where it's worth paying more, and the areas to skip. The Loop, River North and the Gold Coast compared."),
("Chicago on a budget?","where to stay without overpaying","Where to Stay in Chicago on a Budget","Smart Chicago neighborhoods near the sights and transit without the high price tag. Where to stay on a budget for a first trip, with the best-value areas and honest tips."),
],
"Chicago Travel Costs":[
("Is Chicago expensive?","the honest answer, in real numbers","Chicago Travel Costs: An Honest Budget Guide","Is Chicago expensive? The honest answer in real numbers: hotels, food, attractions and transit. What a Chicago trip actually costs, with the swaps that bring it down. A realistic budget guide."),
("What 3 days in Chicago cost us","dollar by dollar","What 3 Days in Chicago Actually Cost","A realistic Chicago trip, line by line: hotel, deep dish, the architecture cruise, the Skydeck and transit. What 3 days in Chicago actually cost us, plus where to save."),
("Chicago on a budget?","yes, here's how","Chicago on a Budget: How to Visit for Less","Chicago on a budget is easy if you know where to look. The big expenses and the smart swaps, from free lakefront views to cheap eats. How to do Chicago for less."),
("Where to splurge, where to save","in Chicago","Chicago Travel Costs: Where to Splurge and Save","The Chicago experiences worth paying for (the architecture cruise, the Skydeck) and the ones to do free: a smarter way to budget your trip. With honest splurge-or-skip calls."),
],
"20 Free Things to Do in Chicago":[
("The best free things to do in Chicago","that still wow","Free Things to Do in Chicago That Still Wow","The Bean, the lakefront, free museum days and the Lincoln Park Zoo: the best free things to do in Chicago that still feel like the real thing. How to experience the city without spending."),
("Chicago for free","the best no-cost spots","20 Free Things to Do in Chicago","Millennium Park, the Riverwalk, the lakefront trail and free museum days: how to experience Chicago for next to nothing. The best free things to do for budget-conscious first-timers."),
("Chicago on zero dollars?","here's how to do it","Free Things to Do in Chicago on a Budget","Beaches, parks, the Bean and free museum hours: how to enjoy Chicago without spending. The best free things to do for a budget first trip to the city."),
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
