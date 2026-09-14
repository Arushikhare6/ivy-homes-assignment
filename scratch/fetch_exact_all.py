import urllib.request
import urllib.parse
import json
import os

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

def fetch_exact_endpoint(endpoint_name, path):
    print(f"=== Fetching exact {endpoint_name} ===")
    all_records = []
    offset = 0
    batch_limit = 50

    while True:
        res = api_req(path, {"offset": offset, "limit": batch_limit}, headers=headers)
        results = res.get("results", [])
        if not results:
            print(f"  Reached end of {endpoint_name} at offset {offset}. Total fetched = {len(all_records)}")
            break
        all_records.extend(results)
        print(f"  Offset {offset:4d}: fetched {len(results):2d} items. Cumulative = {len(all_records)}")
        offset += len(results)

    with open(os.path.join(DATA_DIR, f"{endpoint_name}_exact.json"), "w") as f:
        json.dump(all_records, f, indent=2)

    return all_records

listings = fetch_exact_endpoint("listings", "/v1/listings")
rentals = fetch_exact_endpoint("rentals", "/v1/rentals")
projects = fetch_exact_endpoint("projects", "/v1/projects")

print("\nExact datasets saved successfully!")
