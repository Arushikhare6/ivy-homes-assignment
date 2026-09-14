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

page1 = api_req("/v1/listings", {"page": 1}, headers=headers)
page2 = api_req("/v1/listings", {"page": 2}, headers=headers)

p1_ids = [l["listing_id"] for l in page1.get("results", [])]
p2_ids = [l["listing_id"] for l in page2.get("results", [])]

print("Page 1 first 5 IDs:", p1_ids[:5])
print("Page 2 first 5 IDs:", p2_ids[:5])
print("Are Page 1 and Page 2 identical?", p1_ids == p2_ids)

# Let's check rentals page 1 vs page 2
r_page1 = api_req("/v1/rentals", {"page": 1}, headers=headers)
r_page2 = api_req("/v1/rentals", {"page": 2}, headers=headers)
rp1_ids = [r["listing_id"] for r in r_page1.get("results", [])]
rp2_ids = [r["listing_id"] for r in r_page2.get("results", [])]
print("\nRentals Page 1 first 5 IDs:", rp1_ids[:5])
print("Rentals Page 2 first 5 IDs:", rp2_ids[:5])
print("Are Rentals Page 1 and Page 2 identical?", rp1_ids == rp2_ids)

# Let's check projects page 1 vs page 2
pr_page1 = api_req("/v1/projects", {"page": 1}, headers=headers)
pr_page2 = api_req("/v1/projects", {"page": 2}, headers=headers)
pr1_ids = [p["project_id"] for p in pr_page1.get("results", [])]
pr2_ids = [p["project_id"] for p in pr_page2.get("results", [])]
print("\nProjects Page 1 first 5 IDs:", pr1_ids[:5])
print("Projects Page 2 first 5 IDs:", pr2_ids[:5])
print("Are Projects Page 1 and Page 2 identical?", pr1_ids == pr2_ids)

