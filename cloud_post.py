# -*- coding: utf-8 -*-
"""Cloud poster for GitHub Actions.
Refreshes the Pinterest access token from a long-lived refresh token (kept in GitHub Secrets),
then posts every pin whose scheduled time (Europe/Budapest) has arrived and isn't posted yet.
Dependency-free (urllib). Times in pins.csv are treated as Europe/Budapest local time."""
import os, csv, json, base64, glob, urllib.request, urllib.parse, datetime
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(os.path.abspath(__file__))
TZ = ZoneInfo("Europe/Budapest")
API = "https://api.pinterest.com/v5"
POSTED = os.path.join(ROOT, "posted.json")

# Safety window: a "due but not logged as posted" row is only caught up if its
# scheduled time is within this many hours of now. Without this, editing the
# URL/slug of an already-posted row (which changes its posted.json key) makes
# cloud_post.py think it was never posted and re-post it, however old the date --
# this is exactly how two accidental duplicate posts happened (2026.07.09
# millennium-park-cloud-gate-chicago pin1 posted 5 days late on 07.14, and
# 2026.07.08 best-things-to-do-in-chicago pin1 posted 14 days late on 07.22).
MAX_CATCHUP_HOURS = 48

CID = os.environ["PINTEREST_CLIENT_ID"]
CSECRET = os.environ["PINTEREST_CLIENT_SECRET"]
REFRESH = os.environ["PINTEREST_REFRESH_TOKEN"]
ACCESS = None


def _post_form(path, form, auth_header):
    data = urllib.parse.urlencode(form).encode()
    req = urllib.request.Request(API + path, data=data, method="POST",
        headers={"Authorization": auth_header, "Content-Type": "application/x-www-form-urlencoded"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def refresh_access_token():
    basic = base64.b64encode(f"{CID}:{CSECRET}".encode()).decode()
    d = _post_form("/oauth/token", {"grant_type": "refresh_token", "refresh_token": REFRESH}, "Basic " + basic)
    return d["access_token"]


def api(path, method="GET", body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(API + path, data=data, method=method,
        headers={"Authorization": "Bearer " + ACCESS, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def get_boards():
    boards, bm = {}, None
    while True:
        d = api("/boards?page_size=100" + (f"&bookmark={urllib.parse.quote(bm)}" if bm else ""))
        for b in d.get("items", []):
            boards[b["name"].strip().lower()] = b["id"]
        bm = d.get("bookmark")
        if not bm:
            break
    return boards


def fetch_recent_titles(max_pages=3, window_hours=6):
    """Titles posted to Pinterest within the last `window_hours`. This catches a GENUINE
    near-duplicate (a pin re-posted minutes ago by a run whose posted.json push failed),
    but deliberately does NOT block a pin that merely reuses a title from days ago
    (different image, different scheduled pin). Pins are returned newest-first, so we can
    stop once we pass the window. Returns {lowercased_title: pin_id}. Fails soft."""
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=window_hours)
    titles, bm = {}, None
    try:
        for _ in range(max_pages):
            d = api("/pins?page_size=100" + (f"&bookmark={urllib.parse.quote(bm)}" if bm else ""))
            stop = False
            for p in d.get("items", []):
                ca = (p.get("created_at") or "").replace("Z", "+00:00")
                try:
                    cdt = datetime.datetime.fromisoformat(ca)
                    if cdt.tzinfo is None:
                        cdt = cdt.replace(tzinfo=datetime.timezone.utc)
                except Exception:
                    continue  # can't confirm recency -> don't guard on it
                if cdt < cutoff:
                    stop = True
                    break  # newest-first: everything after this is older too
                t = (p.get("title") or "").strip().lower()
                if t:
                    titles[t] = p.get("id")
            bm = d.get("bookmark")
            if stop or not bm:
                break
    except Exception as e:
        print(f"WARN: could not fetch recent pins ({e}); posting without dup-guard this run")
    return titles


def slug_of(url):
    url = url.split("#")[0]  # strip anchor fragment before computing slug
    return url.replace("https://milesandflavors.com/", "").strip("/")


def find_image(slug, pin_no, datum):
    # Scope by date first: the same slug+pin repeats across cycles (e.g. Pin1
    # posted 07.08, then again 07.23), and a bare "*{slug}_pin{N}.png" glob
    # would match every cycle's render with no guaranteed order -- glob.glob()
    # is not sorted, so it can silently return an old cycle's stale image
    # instead of the one actually due today.
    dated = glob.glob(os.path.join(ROOT, "done", f"{datum}_*_{slug}_pin{pin_no}.png"))
    if dated:
        return sorted(dated, key=os.path.getmtime, reverse=True)[0]
    g = glob.glob(os.path.join(ROOT, "done", f"*{slug}_pin{pin_no}.png"))
    return g[0] if g else None


def main():
    global ACCESS
    ACCESS = refresh_access_token()
    boards = get_boards()
    recent = fetch_recent_titles()   # dup-guard: titles already live on Pinterest
    posted = json.load(open(POSTED, encoding="utf-8")) if os.path.exists(POSTED) else {}
    now = datetime.datetime.now(TZ)

    rows = list(csv.reader(open(os.path.join(ROOT, "pins.csv"), encoding="utf-8-sig"), delimiter=";"))
    h = {n: i for i, n in enumerate(rows[0])}

    posted_count = 0
    for r in rows[1:]:
        try:
            dt = datetime.datetime.strptime(r[h["Datum"]] + " " + r[h["Idopont"]], "%Y.%m.%d %H:%M").replace(tzinfo=TZ)
        except Exception:
            continue
        slug = slug_of(r[h["URL"]]); pin = r[h["Pin #"]]
        key = f"{r[h['Datum']]}_{slug}_pin{pin}"
        if dt > now or key in posted:
            continue
        stale_hours = (now - dt).total_seconds() / 3600
        if stale_hours > MAX_CATCHUP_HOURS:
            print(f"SKIP (stale {stale_hours/24:.1f}d, not logged under current slug -- check for a URL/slug edit): {key}")
            continue
        board_id = boards.get(r[h["Board"]].strip().lower())
        img = find_image(slug, pin, r[h["Datum"]])
        if not board_id:
            print(f"SKIP (no board): {r[h['Board']]} | {r[h['Cikk']]}"); continue
        if not img:
            print(f"SKIP (no image): {slug}_pin{pin}"); continue
        title = r[h["Pin cim"]][:100]
        tkey = title.strip().lower()
        if tkey in recent:
            # Already on Pinterest (e.g. a parallel run posted it). Record + skip, never re-post.
            posted[key] = {"pin_id": recent[tkey], "at": now.isoformat(), "note": "already-on-pinterest"}
            print(f"SKIP (already on Pinterest): {key}")
            continue
        b64 = base64.b64encode(open(img, "rb").read()).decode()
        body = {"board_id": board_id, "title": title, "description": r[h["Pin leiras"]][:500],
                "link": r[h["URL"]], "alt_text": r[h["Alt text"]][:500],
                "media_source": {"source_type": "image_base64", "content_type": "image/png", "data": b64}}
        try:
            res = api("/pins", "POST", body)
            posted[key] = {"pin_id": res.get("id"), "at": now.isoformat()}
            recent[tkey] = res.get("id")
            posted_count += 1
            print(f"POSTED {r[h['Idopont']]} {r[h['Cikk']][:34]} -> {res.get('id')}")
        except Exception as e:
            print(f"ERROR posting {key}: {e}")

    json.dump(posted, open(POSTED, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Done. Newly posted this run: {posted_count} | total logged: {len(posted)} | now(Budapest)={now:%Y-%m-%d %H:%M}")


if __name__ == "__main__":
    main()
