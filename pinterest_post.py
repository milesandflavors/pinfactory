# -*- coding: utf-8 -*-
"""Pinterest poster. Reads pins.csv, finds rendered images in done/, posts via Pinterest API.
  python pinterest_post.py boards   -> fetch your boards, reconcile with the plan, report missing
  python pinterest_post.py test     -> post ONE pin right now (verify the whole chain works)
  python pinterest_post.py due      -> post every pin whose scheduled time has passed (not yet posted)
  python pinterest_post.py loop     -> keep running; posts each pin when its time arrives (watch it live)
"""
import json, os, base64, glob, csv, time, datetime, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
API = "https://api.pinterest.com/v5"
tok = json.load(open(os.path.join(ROOT, "tokens.json"), encoding="utf-8"))
ACCESS = tok["access_token"]
POSTED = os.path.join(ROOT, "posted.json")
posted = json.load(open(POSTED)) if os.path.exists(POSTED) else {}

def _req(path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    headers = {"Authorization": "Bearer " + ACCESS}
    if body is not None: headers["Content-Type"] = "application/json"
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        print("  API ERROR", e.code, e.read().decode()[:300]); raise

def get_boards():
    boards, bm = {}, None
    while True:
        d = _req("/boards?page_size=100" + (f"&bookmark={urllib.parse.quote(bm)}" if bm else ""))
        for b in d.get("items", []): boards[b["name"].strip().lower()] = b["id"]
        bm = d.get("bookmark")
        if not bm: break
    return boards

def rows():
    r = list(csv.reader(open(os.path.join(ROOT, "pins.csv"), encoding="utf-8-sig"), delimiter=";"))
    h = {n: i for i, n in enumerate(r[0])}
    return h, r[1:]

def find_image(slug, pin_no):
    g = glob.glob(os.path.join(ROOT, "done", f"*{slug}_pin{pin_no}.png"))
    return g[0] if g else None

def slug_of(url): return url.replace("https://milesandflavors.com/", "").strip("/")

def post_one(h, r, boards):
    board_name = r[h["Board"]].strip().lower()
    bid = boards.get(board_name)
    slug = slug_of(r[h["URL"]]); pin_no = r[h["Pin #"]]
    img = find_image(slug, pin_no)
    key = f"{r[h['Datum']]}_{slug}_pin{pin_no}"
    if not bid: return ("no_board", board_name)
    if not img: return ("no_image", f"{slug}_pin{pin_no}")
    b64 = base64.b64encode(open(img, "rb").read()).decode()
    body = {"board_id": bid, "title": r[h["Pin cim"]][:100], "description": r[h["Pin leiras"]][:500],
            "link": r[h["URL"]], "alt_text": r[h["Alt text"]][:500],
            "media_source": {"source_type": "image_base64", "content_type": "image/png", "data": b64}}
    res = _req("/pins", "POST", body)
    posted[key] = {"pin_id": res.get("id"), "at": datetime.datetime.now().isoformat()}
    json.dump(posted, open(POSTED, "w"), indent=2)
    return ("ok", res.get("id"))

def due_now(h, r):
    dt = datetime.datetime.strptime(r[h["Datum"]] + " " + r[h["Idopont"]], "%Y.%m.%d %H:%M")
    slug = slug_of(r[h["URL"]]); key = f"{r[h['Datum']]}_{slug}_pin{r[h['Pin #']]}"
    return dt <= datetime.datetime.now() and key not in posted

def cmd_boards():
    boards = get_boards()
    json.dump(boards, open(os.path.join(ROOT, "boards.json"), "w"), indent=2, ensure_ascii=False)
    print(f"Your Pinterest boards ({len(boards)}):")
    for n in sorted(boards): print("   -", n)
    h, rs = rows()
    need = sorted(set(r[h["Board"]].strip() for r in rs))
    missing = [b for b in need if b.strip().lower() not in boards]
    print(f"\nBoards the plan uses: {len(need)}")
    if missing:
        print(f"!! MISSING ({len(missing)}) — create these on Pinterest (same name) so pins can post there:")
        for b in missing: print("   x", b)
    else:
        print("All plan boards exist on your account. Ready to post.")

def cmd_test():
    boards = get_boards()
    h, rs = rows()
    day1 = sorted([r for r in rs if r[h["Datum"]] == "2026.06.06"],
                  key=lambda r: datetime.datetime.strptime(r[h["Datum"]] + " " + r[h["Idopont"]], "%Y.%m.%d %H:%M"))
    r = day1[0]
    print("Test-posting:", r[h["Cikk"]], "| board:", r[h["Board"]])
    print(" ->", post_one(h, r, boards))

def cmd_due():
    boards = get_boards()
    h, rs = rows()
    todo = [r for r in rs if due_now(h, r)]
    print(f"Due pins to post now: {len(todo)}")
    for r in todo:
        st = post_one(h, r, boards)
        print(f"   {r[h['Idopont']]:>6} {r[h['Cikk']][:34]:34} -> {st}")

def cmd_loop():
    print("Live mode: checking every 60s, posting each pin when its time arrives. Ctrl+C to stop.")
    boards = get_boards()
    while True:
        h, rs = rows()
        for r in rs:
            if due_now(h, r):
                st = post_one(h, r, boards)
                print(f"[{datetime.datetime.now():%H:%M}] {r[h['Cikk']][:34]:34} -> {st}", flush=True)
        time.sleep(60)

def cmd_day1():
    boards = get_boards()
    h, rs = rows()
    day1 = sorted([r for r in rs if r[h["Datum"]] == "2026.06.06"],
                  key=lambda r: datetime.datetime.strptime(r[h["Datum"]] + " " + r[h["Idopont"]], "%Y.%m.%d %H:%M"))
    print(f"Posting all {len(day1)} Day-1 pins...")
    for r in day1:
        st = post_one(h, r, boards)
        print(f"   {r[h['Idopont']]:>6} {r[h['Cikk']][:32]:32} -> {st}")

{"boards": cmd_boards, "test": cmd_test, "due": cmd_due, "loop": cmd_loop, "day1": cmd_day1}.get(
    sys.argv[1] if len(sys.argv) > 1 else "boards", cmd_boards)()
