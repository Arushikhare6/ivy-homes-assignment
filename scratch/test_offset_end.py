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

def find_dataset_end(endpoint, name):
    print(f"\n=== Finding end for {name} ({endpoint}) ===")
    first_res = api_req(endpoint, {"offset": 0, "limit": 50}, headers=headers)
    reported_total = first_res.get("total")
    print(f"Reported total: {reported_total}")

    # Let's test offset = reported_total - 10, reported_total, reported_total + 10, etc.
    for off in range(max(0, reported_total - 50), reported_total + 100, 10):
        res = api_req(endpoint, {"offset": off, "limit": 50}, headers=headers)
        results = res.get("results", [])
        print(f"  Offset {off:5d}: returned {len(results):2d} items.")
        if len(results) == 0:
            print(f"  --> END FOUND AT OFFSET {off}!")
            break

find_dataset_end("/v1/listings", "Listings")
find_dataset_end("/v1/rentals", "Rentals")
find_dataset_end("/v1/projects", "Projects")

