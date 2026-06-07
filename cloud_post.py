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


def slug_of(url):
    return url.replace("https://milesandflavors.com/", "").strip("/")


def find_image(slug, pin_no):
    g = glob.glob(os.path.join(ROOT, "done", f"*{slug}_pin{pin_no}.png"))
    return g[0] if g else None


def main():
    global ACCESS
    ACCESS = refresh_access_token()
    boards = get_boards()
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
        board_id = boards.get(r[h["Board"]].strip().lower())
        img = find_image(slug, pin)
        if not board_id:
            print(f"SKIP (no board): {r[h['Board']]} | {r[h['Cikk']]}"); continue
        if not img:
            print(f"SKIP (no image): {slug}_pin{pin}"); continue
        b64 = base64.b64encode(open(img, "rb").read()).decode()
        body = {"board_id": board_id, "title": r[h["Pin cim"]][:100], "description": r[h["Pin leiras"]][:500],
                "link": r[h["URL"]], "alt_text": r[h["Alt text"]][:500],
                "media_source": {"source_type": "image_base64", "content_type": "image/png", "data": b64}}
        try:
            res = api("/pins", "POST", body)
            posted[key] = {"pin_id": res.get("id"), "at": now.isoformat()}
            posted_count += 1
            print(f"POSTED {r[h['Idopont']]} {r[h['Cikk']][:34]} -> {res.get('id')}")
        except Exception as e:
            print(f"ERROR posting {key}: {e}")

    json.dump(posted, open(POSTED, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"Done. Newly posted this run: {posted_count} | total logged: {len(posted)} | now(Budapest)={now:%Y-%m-%d %H:%M}")


if __name__ == "__main__":
    main()
