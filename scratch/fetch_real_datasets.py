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

def log(msg):
    print(msg, flush=True)

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

def fetch_all_by_offset(endpoint_name, path, limit_val=50):
    log(f"=== Fetching {endpoint_name} via OFFSET pagination ===")
    first_resp = api_req(path, {"offset": 0, "limit": limit_val}, headers=headers)
    total = first_resp.get("total", 0)
    page_1_results = first_resp.get("results", [])
    batch_size = len(page_1_results) if len(page_1_results) > 0 else limit_val

    log(f"{endpoint_name}: total reported = {total}, first batch size = {batch_size}")

    offsets = list(range(batch_size, total, batch_size))
    
    results_map = {0: page_1_results}

    def fetch_batch(off):
        resp = api_req(path, {"offset": off, "limit": limit_val}, headers=headers)
        return off, resp.get("results", [])

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(fetch_batch, off) for off in offsets]
        for future in as_completed(futures):
            off, res_list = future.result()
            results_map[off] = res_list

    all_records = []
    for off in sorted(results_map.keys()):
        all_records.extend(results_map[off])

    log(f"Finished {endpoint_name}: Total retrieved = {len(all_records)} / Total reported = {total}")

    with open(os.path.join(DATA_DIR, f"{endpoint_name}_true.json"), "w") as f:
        json.dump(all_records, f, indent=2)

    return all_records

listings = fetch_all_by_offset("listings", "/v1/listings")
rentals = fetch_all_by_offset("rentals", "/v1/rentals")
projects = fetch_all_by_offset("projects", "/v1/projects")

log("\nTrue dataset download finished successfully!")
