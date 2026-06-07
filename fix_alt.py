# -*- coding: utf-8 -*-
"""Rewrite the Alt text column for every pin as a real SCENE description of the
image (not a title repetition). Scenes are picked per destination + topic and
rotated by pin number so pins of the same article get varied alt text."""
import csv, os

def cl(s):
    if 'athens' in s: return 'Athens'
    if 'zakynthos' in s or 'shipwreck' in s: return 'Zakynthos'
    if 'greece' in s: return 'Greece'
    if 'rome' in s: return 'Rome'
    if 'nyc' in s or 'new-york' in s: return 'NYC'
    if 'amalfi' in s or 'southern-italy' in s: return 'Amalfi'
    if 'dolomite' in s: return 'Dolomites'
    if 'milan' in s: return 'Milan'
    if 'barcelona' in s: return 'Barcelona'
    if 'amsterdam' in s: return 'Amsterdam'
    if 'chicago' in s: return 'Chicago'
    if 'kyoto' in s: return 'Kyoto'
    if 'osaka' in s: return 'Osaka'
    if 'tokyo' in s or 'hakone' in s or 'ryokan' in s: return 'Tokyo'
    if 'japan' in s: return 'Japan'
    if 'marsa' in s: return 'Egypt'
    return 'Planning'

# Generic destination scene banks (vivid, describe what's in the photo)
SCENES = {
'Barcelona':[
 "The colorful mosaic curves of Park Guell overlooking Barcelona and the sea.",
 "Sunlight on the soaring spires of Gaudi's Sagrada Familia in Barcelona, Spain.",
 "A narrow, atmospheric stone street in Barcelona's Gothic Quarter.",
 "The Barcelona skyline glowing at sunset, seen from a hilltop viewpoint.",
 "Palm trees and golden sand along the beachfront in Barcelona.",
 "An ornate Gaudi facade with colorful tiles in Barcelona, Spain.",
],
'Rome':[
 "The ancient arches of the Roman Colosseum glowing in the afternoon light.",
 "Water cascading over the marble figures of the Trevi Fountain in Rome.",
 "The open dome of the Pantheon above a sunlit piazza in Rome, Italy.",
 "Ivy-draped lanes and warm stone buildings in Rome's Trastevere district.",
 "The ruins of the Roman Forum beneath a soft golden sky.",
 "A cobbled Roman street lined with terracotta buildings and cafes.",
],
'Amalfi':[
 "The pastel houses of Positano tumbling down to the turquoise sea on the Amalfi Coast.",
 "A cliffside view over the deep blue water of the Amalfi Coast, Italy.",
 "Lemon groves and terraces above the sea on the Amalfi Coast.",
 "Colorful Italian buildings and a tiled church dome on the Amalfi Coast.",
 "A winding coastal road and dramatic cliffs along the Amalfi Coast.",
 "Boats dotting the sparkling blue water below an Amalfi Coast village.",
],
'Dolomites':[
 "A hiking trail leading through the dramatic limestone peaks of the Dolomites in northern Italy.",
 "The turquoise water of Lago di Braies beneath towering Dolomite peaks.",
 "Jagged Dolomite mountains rising above green alpine meadows.",
 "A wooden mountain hut and wildflower meadow in the Italian Dolomites.",
 "Golden sunrise light on the rugged peaks of the Dolomites.",
 "A still alpine lake reflecting the sheer cliffs of the Dolomites.",
],
'Milan':[
 "The ornate marble spires of the Duomo cathedral in Milan, Italy.",
 "An elegant glass-roofed shopping gallery in central Milan.",
 "A lively Milan piazza with historic architecture and cafes.",
],
'Athens':[
 "The ancient marble columns of the Acropolis rising above the city of Athens, Greece.",
 "The Parthenon glowing at golden hour atop the Acropolis in Athens.",
 "A charming cafe-lined street in the Plaka district below the Acropolis in Athens.",
 "Whitewashed rooftops of Athens stretching toward the Acropolis hill.",
 "Ancient ruins and olive trees in the heart of Athens, Greece.",
 "A rooftop view over Athens with the floodlit Acropolis at dusk.",
],
'Greece':[
 "A sun-drenched Greek island view with white buildings above the deep blue Aegean Sea.",
 "Whitewashed houses and blue domes overlooking the sea in Greece.",
 "A turquoise cove framed by dramatic cliffs on a Greek island.",
 "A traditional Greek taverna with sea views and pink bougainvillea.",
 "A ferry crossing the sparkling blue water between Greek islands.",
 "A pastel sunset over the caldera and white villages of a Greek island.",
],
'Zakynthos':[
 "The famous Navagio Shipwreck Beach with its rusting wreck and turquoise water in Zakynthos.",
 "Sheer white cliffs above the impossibly blue water of a Zakynthos beach.",
 "A small boat floating on the clear turquoise sea near the Blue Caves of Zakynthos.",
 "A hidden cove with crystal-clear water on the coast of Zakynthos, Greece.",
 "Sunbathers on golden sand beside the bright blue Ionian Sea in Zakynthos.",
],
'NYC':[
 "The New York City skyline of towering skyscrapers on a bright, clear day.",
 "Yellow taxis and tall buildings on a busy street in New York City.",
 "The Brooklyn Bridge stretching toward the Manhattan skyline at sunset.",
 "Autumn colors in Central Park with skyscrapers rising behind the trees.",
 "The glowing billboards and crowds of Times Square in New York City at night.",
 "A classic New York City brownstone street lined with steps and trees.",
],
'Tokyo':[
 "The neon-lit streets and crowds of the Shibuya crossing in Tokyo, Japan.",
 "A traditional red temple gate against the modern Tokyo skyline.",
 "Glowing lanterns and signs in a narrow Tokyo backstreet at night.",
 "Cherry blossoms framing a canal in springtime Tokyo, Japan.",
 "Snow-capped Mount Fuji rising above a calm lake near Tokyo.",
],
'Kyoto':[
 "Rows of vermilion torii gates winding up the hillside at Fushimi Inari shrine in Kyoto.",
 "The towering green stalks of the Arashiyama bamboo grove in Kyoto.",
 "A golden temple reflected in a still pond in Kyoto, Japan.",
 "A traditional wooden street in the historic Gion district of Kyoto.",
],
'Osaka':[
 "Glowing neon signs and street-food stalls along the Dotonbori canal in Osaka, Japan.",
 "Osaka Castle rising above green gardens under a blue sky.",
 "A lively Osaka street filled with food stalls and bright lights at night.",
 "Steam rising from sizzling street food in a busy Osaka market.",
],
'Japan':[
 "Snow-capped Mount Fuji rising above a calm lake in Japan.",
 "Cherry blossoms framing a traditional temple in Japan.",
 "A bullet train speeding past the Japanese countryside.",
 "Rows of vermilion torii gates on a forested hillside in Japan.",
],
'Chicago':[
 "The mirrored surface of Cloud Gate, the Bean, reflecting the Chicago skyline.",
 "The Chicago skyline rising above the river and downtown architecture.",
 "Tour boats on the Chicago River winding between towering skyscrapers.",
 "The Chicago lakefront and skyline on a clear blue day.",
 "Millennium Park and the city skyline glowing at dusk in Chicago.",
],
'Amsterdam':[
 "A picturesque Amsterdam canal lined with narrow gabled houses and bicycles.",
 "Bridges and houseboats along a tree-lined canal in Amsterdam, Netherlands.",
 "Bicycles parked along a canal bridge in central Amsterdam.",
 "Colorful tulips blooming in front of a row of Amsterdam canal houses.",
 "A canal boat gliding past historic buildings in Amsterdam at golden hour.",
],
'Egypt':[
 "Crystal-clear turquoise water over a coral reef on Egypt's Red Sea coast at Marsa Alam.",
 "A sandy beach meeting the vivid blue Red Sea in Marsa Alam, Egypt.",
 "Colorful coral and tropical fish beneath the surface of the Red Sea.",
 "A calm desert landscape meeting the bright blue Red Sea near Marsa Alam.",
 "A wooden jetty stretching over the clear turquoise water of the Red Sea.",
],
'Planning':[
 "A traveler planning a trip with a map, passport and notebook on a table.",
 "An open suitcase packed for a trip beside a world map.",
 "An airplane wing above a sea of clouds on the way to a new destination.",
 "A person holding a phone and travel documents while planning a journey.",
],
}

# Topic-specific scene overrides (checked against the article title, lowercased)
def topic_scenes(cikk, cluster):
    c = cikk.lower()
    if 'where to stay' in c:
        return [f"A stylish, sunlit hotel room with a comfortable bed and a view, ready for a stay in {place(cluster)}.",
                f"A cozy boutique hotel interior in {place(cluster)}.",
                f"A hotel balcony looking out over the rooftops of {place(cluster)}."]
    if 'cherry blossom' in c:
        return ["Pale pink cherry blossoms in full bloom beside a traditional temple in Japan.",
                "A path lined with blooming cherry blossom trees in springtime Japan."]
    if 'canal cruise' in c:
        return ["A canal boat gliding past historic gabled houses in Amsterdam.",
                "A view from a canal cruise of bridges and reflections in Amsterdam at dusk.",
                "Tourists on an open canal boat passing under a bridge in Amsterdam."]
    if 'money card' in c:
        return ["A traveler holding a bank card and phone, ready to pay abroad without fees.",
                "Travel cards and a smartphone laid out on a map, ready for a trip."]
    if 'cheap flight' in c or 'stopover' in c:
        return ["An airplane taking off into a clear sky, representing finding cheap flights.",
                "A departures board and airplane wing on the way to a new destination."]
    if 'esim' in c:
        return ["A smartphone showing a strong mobile connection while traveling abroad.",
                "A traveler using a phone with a travel eSIM in a foreign city."]
    if 'toddler' in c:
        return ["A family exploring a new destination together with a young child.",
                "A parent and toddler walking hand in hand while traveling."]
    if 'beach destination' in c or ('beach' in c and cluster == 'Planning'):
        return ["A palm-fringed tropical beach with white sand and clear turquoise water.",
                "Turquoise sea lapping a quiet, palm-lined tropical beach."]
    if 'cheap' in c or 'affordable' in c or 'budget' in c:
        return ["A scenic, affordable travel destination with clear skies and open views.",
                "A traveler exploring a beautiful, budget-friendly destination."]
    return None

def place(cluster):
    return {'Athens':'Athens','Zakynthos':'Zakynthos','Greece':'Greece','Rome':'Rome','NYC':'New York City',
            'Amalfi':'the Amalfi Coast','Dolomites':'the Dolomites','Milan':'Milan','Barcelona':'Barcelona',
            'Amsterdam':'Amsterdam','Chicago':'Chicago','Kyoto':'Kyoto','Osaka':'Osaka','Tokyo':'Tokyo',
            'Japan':'Japan','Egypt':'Marsa Alam'}.get(cluster, 'a beautiful destination')

ROOT = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.reader(open(os.path.join(ROOT, "pins.csv"), encoding="utf-8-sig"), delimiter=";"))
h = {n: i for i, n in enumerate(rows[0])}
n = 0
for r in rows[1:]:
    slug = r[h["URL"]].replace("https://milesandflavors.com/", "").strip("/")
    cluster = cl(slug)
    cikk = r[h["Cikk"]]
    bank = topic_scenes(cikk, cluster) or SCENES.get(cluster, SCENES['Planning'])
    pin = int(r[h["Pin #"]])
    r[h["Alt text"]] = bank[(pin - 1) % len(bank)]
    n += 1
with open(os.path.join(ROOT, "pins.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(rows[0]); w.writerows(rows[1:])
print("Alt text rewritten for", n, "pins")
