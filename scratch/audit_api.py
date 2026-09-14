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

print("Starting API Audit with Bearer Token and X-API-Key...")

# 1. Login
login_status, login_res, _ = api_req("/auth/login", data={"email": "demo1@ivy.homes", "password": PASSWORD}, method="POST")
access_token = login_res.get("access_token")
refresh_token = login_res.get("refresh_token")
print(f"Logged in successfully. access_token: {access_token[:20]}...")

auth_headers = {"Authorization": f"Bearer {access_token}"}

# 2. Fetch all listings
print("\nFetching all listings...")
listings_all = []
page = 1
limit = 200

while True:
    st, res, _ = api_req("/v1/listings", query_params={"page": page, "limit": limit}, headers=auth_headers)
    if st != 200:
        print(f"Error fetching page {page}: {st} {res}")
        break
    
    if page == 1:
        print(f"Listings endpoint page 1 header/metadata: total={res.get('total')}, page_size={res.get('page_size')}, page={res.get('page')}")
        print("First listing sample keys:", list(res.get("results", [{}])[0].keys()))
        print("First listing sample:", json.dumps(res.get("results", [{}])[0], indent=2))
    
    results = res.get("results", [])
    listings_all.extend(results)
    print(f"Listings Page {page}: fetched {len(results)} items. Cumulative: {len(listings_all)}")
    
    if len(results) == 0 or len(listings_all) >= res.get("total", 0):
        break
    page += 1

with open(os.path.join(DATA_DIR, "listings.json"), "w") as f:
    json.dump(listings_all, f, indent=2)
print(f"Saved {len(listings_all)} listings to listings.json")

# 3. Fetch all rentals
print("\nFetching all rentals...")
rentals_all = []
page = 1
while True:
    st, res, _ = api_req("/v1/rentals", query_params={"page": page, "limit": limit}, headers=auth_headers)
    if st != 200:
        print(f"Error fetching rentals page {page}: {st} {res}")
        break
    
    if page == 1:
        print(f"Rentals endpoint page 1 metadata: total={res.get('total')}, page_size={res.get('page_size')}")
        print("First rental sample keys:", list(res.get("results", [{}])[0].keys()))
        print("First rental sample:", json.dumps(res.get("results", [{}])[0], indent=2))
    
    results = res.get("results", [])
    rentals_all.extend(results)
    print(f"Rentals Page {page}: fetched {len(results)} items. Cumulative: {len(rentals_all)}")
    if len(results) == 0 or len(rentals_all) >= res.get("total", 0):
        break
    page += 1

with open(os.path.join(DATA_DIR, "rentals.json"), "w") as f:
    json.dump(rentals_all, f, indent=2)
print(f"Saved {len(rentals_all)} rentals to rentals.json")

# 4. Fetch all projects
print("\nFetching all projects...")
projects_all = []
page = 1
while True:
    st, res, _ = api_req("/v1/projects", query_params={"page": page, "limit": limit}, headers=auth_headers)
    if st != 200:
        print(f"Error fetching projects page {page}: {st} {res}")
        break
    
    if page == 1:
        print(f"Projects endpoint page 1 metadata: total={res.get('total')}, page_size={res.get('page_size')}")
        print("First project sample keys:", list(res.get("results", [{}])[0].keys()))
        print("First project sample:", json.dumps(res.get("results", [{}])[0], indent=2))
    
    results = res.get("results", [])
    projects_all.extend(results)
    print(f"Projects Page {page}: fetched {len(results)} items. Cumulative: {len(projects_all)}")
    if len(results) == 0 or len(projects_all) >= res.get("total", 0):
        break
    page += 1

with open(os.path.join(DATA_DIR, "projects.json"), "w") as f:
    json.dump(projects_all, f, indent=2)
print(f"Saved {len(projects_all)} projects to projects.json")

