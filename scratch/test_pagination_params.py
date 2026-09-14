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
p1_ids = [l["listing_id"] for l in page1.get("results", [])]

test_params = [
    {"offset": 50},
    {"skip": 50},
    {"p": 2},
    {"page_num": 2},
    {"start": 50},
    {"cursor": 50},
    {"page": 2, "limit": 50},
    {"offset": 1},
    {"limit": 100},
    {"limit": 1000},
    {"all": "true"},
    {"all": 1}
]

for tp in test_params:
    res = api_req("/v1/listings", tp, headers=headers)
    results = res.get("results", [])
    r_ids = [l["listing_id"] for l in results]
    is_same = (r_ids == p1_ids)
    print(f"Param {tp}: returned {len(results)} items, page reported={res.get('page')}, total reported={res.get('total')}. Same as page 1? {is_same}")
    if not is_same:
        print(f"  --> FOUND DIFFERENT RESULTS FOR {tp}: first ID is {r_ids[0]}")

