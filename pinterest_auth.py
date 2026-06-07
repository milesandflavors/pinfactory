# -*- coding: utf-8 -*-
"""One-time Pinterest OAuth. Opens a local server, you authorize in the browser,
it catches the code and saves access_token + refresh_token to tokens.json."""
import json, os, base64, urllib.parse, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
REDIRECT = "http://localhost:8085/"
SCOPES = "boards:read,boards:write,pins:read,pins:write,user_accounts:read"
API = "https://api.pinterest.com/v5"

sec = json.load(open(os.path.join(ROOT, "secrets.json"), encoding="utf-8"))
CID, CSECRET = sec["client_id"], sec["client_secret"]

auth_url = "https://www.pinterest.com/oauth/?" + urllib.parse.urlencode({
    "client_id": CID, "redirect_uri": REDIRECT, "response_type": "code",
    "scope": SCOPES, "state": "milesandflavors",
})

print("\n=================  STEP: AUTHORIZE  =================")
print("Open this URL in your browser and click 'Give access':\n")
print(auth_url)
print("\n(Waiting for you to authorize... this window stays open.)\n", flush=True)

holder = {}
class H(BaseHTTPRequestHandler):
    def do_GET(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers()
        if "code" in q:
            holder["code"] = q["code"][0]
            self.wfile.write("<h2>Done! Authorization received. You can close this tab and return to the app.</h2>".encode())
        elif "error" in q:
            holder["error"] = q.get("error_description", q.get("error"))[0]
            self.wfile.write(("<h2>Error: " + str(holder["error"]) + "</h2>").encode())
        else:
            self.wfile.write("<h2>Waiting...</h2>".encode())
    def log_message(self, *a): pass

srv = HTTPServer(("localhost", 8085), H)
while "code" not in holder and "error" not in holder:
    srv.handle_request()

if "error" in holder:
    print("AUTH ERROR:", holder["error"]); raise SystemExit(1)

# exchange code -> tokens
basic = base64.b64encode(f"{CID}:{CSECRET}".encode()).decode()
data = urllib.parse.urlencode({
    "grant_type": "authorization_code", "code": holder["code"], "redirect_uri": REDIRECT,
}).encode()
req = urllib.request.Request(API + "/oauth/token", data=data, headers={
    "Authorization": "Basic " + basic, "Content-Type": "application/x-www-form-urlencoded",
})
tok = json.load(urllib.request.urlopen(req))
json.dump(tok, open(os.path.join(ROOT, "tokens.json"), "w"), indent=2)

# quick verify
who = urllib.request.Request(API + "/user_account", headers={"Authorization": "Bearer " + tok["access_token"]})
acc = json.load(urllib.request.urlopen(who))
print("\n=================  SUCCESS  =================")
print("Logged in as:", acc.get("username"))
print("Granted scopes:", tok.get("scope"))
print("Token saved to tokens.json. You can close this window.")
