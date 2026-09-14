import urllib.request
import urllib.parse
import json
import os
import sys

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

    req_headers = {
        "User-Agent": "IvyHomesAudit/1.0", 
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    if headers:
        req_headers.update(headers)

    body_bytes = None
    if data is not None:
        if isinstance(data, (dict, list)):
            body_bytes = json.dumps(data).encode("utf-8")
        elif isinstance(data, str):
            body_bytes = data.encode("utf-8")
        else:
            body_bytes = data

    request = urllib.request.Request(url, data=body_bytes, headers=req_headers, method=method)

    try:
        with urllib.request.urlopen(request) as response:
            res_body = response.read().decode("utf-8")
            status = response.status
            res_headers = dict(response.headers)
            try:
                parsed_json = json.loads(res_body)
                return status, parsed_json, res_headers
            except Exception:
                return status, res_body, res_headers
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            parsed_json = json.loads(err_body)
            return e.code, parsed_json, dict(e.headers)
        except Exception:
            return e.code, err_body, dict(e.headers)

log("1. Authenticating...")
st, login_res, _ = api_req("/auth/login", data={"email": "demo1@ivy.homes", "password": PASSWORD}, method="POST")
log(f"Login status: {st}")
access_token = login_res.get("access_token")
log(f"Token acquired: {access_token[:15]}...")

auth_headers = {"Authorization": f"Bearer {access_token}"}

# 2. Testing Pagination Limit Discrepancy
log("\n2. Testing Pagination limit behavior...")
st_limit_200, res_limit_200, _ = api_req("/v1/listings", query_params={"limit": 200}, headers=auth_headers)
log(f"limit=200 status: {st_limit_200}")
if isinstance(res_limit_200, dict):
    log(f"limit=200 response metadata: total={res_limit_200.get('total')}, page_size={res_limit_200.get('page_size')}, actual_results_len={len(res_limit_200.get('results', []))}")

st_limit_50, res_limit_50, _ = api_req("/v1/listings", query_params={"limit": 50}, headers=auth_headers)
log(f"limit=50 status: {st_limit_50}")
if isinstance(res_limit_50, dict):
    log(f"limit=50 response metadata: total={res_limit_50.get('total')}, page_size={res_limit_50.get('page_size')}, actual_results_len={len(res_limit_50.get('results', []))}")

# Let's fetch all listings using standard limit (e.g. 50 or reported limit)
limit = res_limit_50.get('page_size', 50) if isinstance(res_limit_50, dict) else 50
log(f"\n3. Fetching ALL listings using limit={limit}...")

listings_all = []
page = 1
total_reported = None

while True:
    st, res, _ = api_req("/v1/listings", query_params={"page": page, "limit": limit}, headers=auth_headers)
    if st != 200:
        log(f"Error fetching listings page {page}: {st} {res}")
        break
    
    total_reported = res.get("total")
    results = res.get("results", [])
    listings_all.extend(results)
    log(f"Listings Page {page}: fetched {len(results)} items (cumulative: {len(listings_all)} / reported total: {total_reported})")
    
    if len(results) == 0 or len(listings_all) >= total_reported:
        break
    page += 1

with open(os.path.join(DATA_DIR, "listings.json"), "w") as f:
    json.dump(listings_all, f, indent=2)
log(f"Saved {len(listings_all)} listings to listings.json")

# 4. Fetch all rentals
log(f"\n4. Fetching ALL rentals...")
rentals_all = []
page = 1
while True:
    st, res, _ = api_req("/v1/rentals", query_params={"page": page, "limit": limit}, headers=auth_headers)
    if st != 200:
        log(f"Error fetching rentals page {page}: {st} {res}")
        break
    
    total_reported = res.get("total")
    results = res.get("results", [])
    rentals_all.extend(results)
    log(f"Rentals Page {page}: fetched {len(results)} items (cumulative: {len(rentals_all)} / reported total: {total_reported})")
    
    if len(results) == 0 or len(rentals_all) >= total_reported:
        break
    page += 1

with open(os.path.join(DATA_DIR, "rentals.json"), "w") as f:
    json.dump(rentals_all, f, indent=2)
log(f"Saved {len(rentals_all)} rentals to rentals.json")

# 5. Fetch all projects
log(f"\n5. Fetching ALL projects...")
projects_all = []
page = 1
while True:
    st, res, _ = api_req("/v1/projects", query_params={"page": page, "limit": limit}, headers=auth_headers)
    if st != 200:
        log(f"Error fetching projects page {page}: {st} {res}")
        break
    
    total_reported = res.get("total")
    results = res.get("results", [])
    projects_all.extend(results)
    log(f"Projects Page {page}: fetched {len(results)} items (cumulative: {len(projects_all)} / reported total: {total_reported})")
    
    if len(results) == 0 or len(projects_all) >= total_reported:
        break
    page += 1

with open(os.path.join(DATA_DIR, "projects.json"), "w") as f:
    json.dump(projects_all, f, indent=2)
log(f"Saved {len(projects_all)} projects to projects.json")

log("\nData download finished successfully!")
