import urllib.request
import urllib.parse
import json
import os
import sys
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

# Login
st, login_res, _ = api_req("/auth/login", data={"email": "demo1@ivy.homes", "password": PASSWORD}, method="POST")
access_token = login_res.get("access_token")
auth_headers = {"Authorization": f"Bearer {access_token}"}

def fetch_endpoint(endpoint_name, path):
    log(f"--- Fetching {endpoint_name} ---")
    st, first_page, _ = api_req(path, query_params={"page": 1, "limit": 50}, headers=auth_headers)
    if st != 200 or not isinstance(first_page, dict):
        log(f"Error fetching page 1 of {endpoint_name}: {st} {first_page}")
        return []

    total = first_page.get("total", 0)
    results_page1 = first_page.get("results", [])
    page_size = len(results_page1) if len(results_page1) > 0 else 50
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 1

    log(f"{endpoint_name}: total={total}, total_pages={total_pages}, page1_count={len(results_page1)}")

    all_records = list(results_page1)

    def fetch_single_page(p):
        s, res, _ = api_req(path, query_params={"page": p, "limit": 50}, headers=auth_headers)
        if s == 200 and isinstance(res, dict):
            return p, res.get("results", [])
        return p, []

    with ThreadPoolExecutor(max_workers=15) as executor:
        futures = [executor.submit(fetch_single_page, p) for p in range(2, total_pages + 1)]
        pages_dict = {}
        for future in as_completed(futures):
            p, res_list = future.result()
            pages_dict[p] = res_list

    for p in range(2, total_pages + 1):
        all_records.extend(pages_dict.get(p, []))

    log(f"Finished {endpoint_name}: total retrieved={len(all_records)}")
    
    with open(os.path.join(DATA_DIR, f"{endpoint_name}.json"), "w") as f:
        json.dump(all_records, f, indent=2)
        
    return all_records

# Kill background task-46 first or let it run / cancel
listings = fetch_endpoint("listings", "/v1/listings")
rentals = fetch_endpoint("rentals", "/v1/rentals")
projects = fetch_endpoint("projects", "/v1/projects")

log("Concurrent download completed successfully!")
