# -*- coding: utf-8 -*-
"""Remove the words 'save' and 'click' from the pin copy columns (our rule: no save/click).
Meaning-preserving synonyms only. Order matters (specific before generic)."""
import csv, os, re

COLS = ["Pin bold (vastag)", "Pin light (vekony)", "Pin cim", "Pin leiras"]

# ordered list of (old -> new); specific phrases first
REPL = [
    ("first trip click", "first trip work"),                         # all 7 'click'
    ("plus where to save", "plus where to cut costs"),               # before generic 'where to save'
    ("where to save", "where to spend less"),                        # the 'Where to splurge, where to save' hook
    ("Where to Splurge and Save", "Where to Splurge and Cut Back"),  # title
    ("splurge-or-save", "splurge-or-skip"),
    ("saves your feet", "spares your feet"),
    ("Which travel card actually saves you money?", "Which travel card actually pays off?"),
    ("Which One Saves You Most", "Which One Wins"),
    ("saves you the most abroad", "keeps the most in your pocket abroad"),
    ("the pass that saves money", "the pass that cuts the cost"),
    ("that save you money", "that cut the cost"),
    ("Secrets to Save Money", "Secrets to Spend Less"),
    ("secrets that save real money", "secrets that genuinely cut costs"),
    ("that save money and keep you walking", "that cost less and keep you walking"),
]

ROOT = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.reader(open(os.path.join(ROOT, "pins.csv"), encoding="utf-8-sig"), delimiter=";"))
h = {n: i for i, n in enumerate(rows[0])}

counts = {}
for r in rows[1:]:
    for c in COLS:
        v = r[h[c]]
        for old, new in REPL:
            if old in v:
                counts[old] = counts.get(old, 0) + v.count(old)
                v = v.replace(old, new)
        r[h[c]] = v

with open(os.path.join(ROOT, "pins.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(rows[0]); w.writerows(rows[1:])

print("Replacements applied:")
for old, new in REPL:
    print(f"  {counts.get(old,0):>2}x  '{old}' -> '{new}'")

# verify none remain
pat = re.compile(r"\b(save|saves|saving|click|clicks)\b", re.I)
left = []
for r in rows[1:]:
    for c in COLS:
        for m in pat.finditer(r[h[c]]):
            left.append((r[h["Cikk"]], c, r[h[c]][max(0,m.start()-20):m.end()+20]))
print(f"\nRemaining save/click in copy columns: {len(left)}")
for cikk, c, ctx in left:
    print(f"   [{cikk}] {c}: ...{ctx}...")
