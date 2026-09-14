import urllib.request
import urllib.parse
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://solve.ivy.homes"
API_KEY = "IVY26-F90E52596CBD"
PASSWORD = "5ec43320d2"
DATA_DIR = r"C:\Users\arushi khare\.gemini\antigravity\brain\9e4ee355-335e-48a8-93dd-6b51a285a691\scratch\data"

os.makedirs(DATA_DIR, exist_ok=True)

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

def fast_fetch_exact(name, path, known_max=4500):
    print(f"=== Fast Fetching {name} ({path}) ===")
    offsets = list(range(0, known_max, 50))
    results_dict = {}

    def fetch_off(off):
        res = api_req(path, {"offset": off, "limit": 50}, headers=headers)
        items = res.get("results", [])
        return off, items

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(fetch_off, off) for off in offsets]
        for f in as_completed(futures):
            off, items = f.result()
            if items:
                results_dict[off] = items

    all_records = []
    for off in sorted(results_dict.keys()):
        all_records.extend(results_dict[off])

    print(f"  Finished {name}: Total fetched = {len(all_records)}")
    with open(os.path.join(DATA_DIR, f"{name}_exact.json"), "w") as f:
        json.dump(all_records, f, indent=2)
    return all_records

fast_fetch_exact("listings", "/v1/listings", 4200)
fast_fetch_exact("rentals", "/v1/rentals", 1600)
fast_fetch_exact("projects", "/v1/projects", 500)

print("\nFast exact download finished!")
