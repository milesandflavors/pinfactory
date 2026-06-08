# -*- coding: utf-8 -*-
"""Review pass 2: per-pin photo swaps (copies fitting photos + writes override map)."""
import os, json, shutil
ROOT = os.path.dirname(os.path.abspath(__file__)); IMG = os.path.join(ROOT, "input_images")
MARSA = "best-things-to-do-in-marsa-alam-egypt-including-the-one-that-changes-everything"

# copies: (src relative to input_images) -> dest folder slug
COPIES = [
 ("day-trip-to-the-dolomites-from-venice/getty-images-UZeTJ2ebMX8-unsplash.jpg", "hiking-in-the-dolomites"),
 ("3-days-in-chicago-itinerary/christopher-alvarenga-LIJpLOX9dQs-unsplash.jpg", "chicago-bucket-list-25-best-things-to-do"),
 ("free-things-to-do-in-marsa-alam/rafal-danhoffer-pjhlt7FZlkk-unsplash.jpg", MARSA),
 ("free-things-to-do-in-marsa-alam/rafal-danhoffer-pjhlt7FZlkk-unsplash.jpg", "where-to-stay-in-marsa-alam"),
 ("where-to-stay-in-marsa-alam/antek-jXsHujSYrfw-unsplash.jpg", MARSA),
 ("best-canal-cruises-in-amsterdam/getty-images-zZwdWxh3YiQ-unsplash.jpg", "where-to-stay-in-amsterdam"),
 ("free-things-to-do-in-marsa-alam/pascal-van-de-vendel-CNdMGaVEozQ-unsplash.jpg", "7-days-in-marsa-alam-itinerary"),
]
for src, dest in COPIES:
    s = os.path.join(IMG, src); d = os.path.join(IMG, dest)
    os.makedirs(d, exist_ok=True); fn = os.path.basename(src)
    if os.path.exists(s):
        shutil.copy(s, os.path.join(d, fn)); print(f"  copied {fn} -> {dest}")
    else:
        print(f"  !! MISSING SRC: {src}")

OVERRIDES = {
 "best-beaches-in-zakynthos_pin2": "nikos-balafas-lRd6MwZAZnE-unsplash.jpg",
 "25-best-things-to-do-in-nyc_pin3": "patrick-tomasso-SVVTZtTGyaU-unsplash.jpg",
 "barcelona-bucket-list_pin3": "pourya-gohari-uoBCga1fNwU-unsplash.jpg",
 "hiking-in-the-dolomites_pin2": "getty-images-UZeTJ2ebMX8-unsplash.jpg",
 f"{MARSA}_pin2": "rafal-danhoffer-pjhlt7FZlkk-unsplash.jpg",
 "where-to-stay-in-marsa-alam_pin2": "rafal-danhoffer-pjhlt7FZlkk-unsplash.jpg",
 f"{MARSA}_pin3": "antek-jXsHujSYrfw-unsplash.jpg",
 "where-to-stay-in-amsterdam_pin2": "getty-images-zZwdWxh3YiQ-unsplash.jpg",
 "chicago-bucket-list-25-best-things-to-do_pin3": "christopher-alvarenga-LIJpLOX9dQs-unsplash.jpg",
 "3-days-in-amsterdam_pin2": "IMG_6627.jpg",
 "7-days-in-marsa-alam-itinerary_pin2": "pascal-van-de-vendel-CNdMGaVEozQ-unsplash.jpg",
}
json.dump(OVERRIDES, open(os.path.join(ROOT, "_photo_overrides.json"), "w", encoding="utf-8"), indent=2)
print("Overrides written:", len(OVERRIDES))
