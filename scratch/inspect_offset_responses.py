import urllib.request
import urllib.parse
import json

BASE_URL = "https://solve.ivy.homes"
API_KEY = "IVY26-F90E52596CBD"
PASSWORD = "5ec43320d2"

def api_req(path, query_params=None, headers=None, method="GET", data=None):
    if query_params is None:
        query_params = {}
    url = BASE_URL + path
    if query_params:
        encoded = urllib.parse.urlencode(query_params)
        url += ("&" if "?" in url else "?") + encoded
    req_headers = {"Content-Type": "application/json", "X-API-Key": API_KEY}
    if headers:
        req_headers.update(headers)
    req = urllib.request.Request(url, data=json.dumps(data).encode() if data else None, headers=req_headers, method=method)
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode())

login_res = api_req("/auth/login", data={"email": "demo1@ivy.homes", "password": PASSWORD}, method="POST")
token = login_res["access_token"]
headers = {"Authorization": f"Bearer {token}"}

offsets_to_test = [0, 20, 40, 50, 60, 100, 200, 500, 1000, 2000, 3000, 3900, 3960, 4000]

print("--- TESTING LISTINGS OFFSETS ---")
for off in offsets_to_test:
    res = api_req("/v1/listings", {"offset": off, "limit": 50}, headers=headers)
    results = res.get("results", [])
    first_id = results[0]["listing_id"] if results else "EMPTY"
    last_id = results[-1]["listing_id"] if results else "EMPTY"
    print(f"Offset {off:4d}: returned {len(results):2d} items. First ID: {first_id}, Last ID: {last_id}")

