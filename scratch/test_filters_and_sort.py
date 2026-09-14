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
    try:
        with urllib.request.urlopen(req) as res:
            return res.status, json.loads(res.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, e.read().decode()

st, login_res = api_req("/auth/login", data={"email": "demo1@ivy.homes", "password": PASSWORD}, method="POST")
token = login_res["access_token"]
refresh_tok = login_res["refresh_token"]
headers = {"Authorization": f"Bearer {token}"}

print("=== 1. TESTING REFRESH ENDPOINT ===")
st_ref, res_ref = api_req("/auth/refresh", data={"refresh_token": refresh_tok}, method="POST")
print(f"POST /auth/refresh status: {st_ref} -> {res_ref}")

print("\n=== 2. TESTING SINGULAR VS PLURAL LISTING PATH ===")
# Doc says: GET /v1/listing/{listing_id}
st_sing, res_sing = api_req("/v1/listing/MAG-4001518", headers=headers)
print(f"GET /v1/listing/MAG-4001518: status {st_sing} -> {res_sing}")

st_plur, res_plur = api_req("/v1/listings/MAG-4001518", headers=headers)
print(f"GET /v1/listings/MAG-4001518: status {st_plur} -> {res_plur}")

print("\n=== 3. TESTING SIMILAR LISTINGS ENDPOINT ===")
st_sim, res_sim = api_req("/v1/listings/MAG-4001518/similar", headers=headers)
print(f"GET /v1/listings/MAG-4001518/similar: status {st_sim} -> {res_sim}")

print("\n=== 4. TESTING FAVOURITES ENDPOINTS ===")
st_fav_get, res_fav_get = api_req("/v1/favourites", headers=headers)
print(f"GET /v1/favourites: status {st_fav_get} -> {res_fav_get}")

st_fav_post, res_fav_post = api_req("/v1/favourites", data={"id": "MAG-4001518"}, method="POST", headers=headers)
print(f"POST /v1/favourites: status {st_fav_post} -> {res_fav_post}")

st_fav_del, res_fav_del = api_req("/v1/favourites/MAG-4001518", method="DELETE", headers=headers)
print(f"DELETE /v1/favourites/MAG-4001518: status {st_fav_del} -> {res_fav_del}")

print("\n=== 5. TESTING FILTERS AND SORTING ON LISTINGS ===")
# Test filter: bhk=3
_, res_bhk3 = api_req("/v1/listings", {"bhk": 3}, headers=headers)
bhk_values = set(l.get("bedroom") for l in res_bhk3.get("results", []))
print(f"Filter bhk=3 returned bedroom values: {bhk_values} (Is filter working? {bhk_values == {3}})")

# Test filter: locality=t nagar
_, res_loc = api_req("/v1/listings", {"locality": "t nagar"}, headers=headers)
localities = set(l.get("locality") for l in res_loc.get("results", []))
print(f"Filter locality='t nagar' returned localities: {localities}")

# Test filter: min_price and max_price
_, res_price = api_req("/v1/listings", {"min_price": 10000000, "max_price": 15000000}, headers=headers)
prices = [l.get("price") for l in res_price.get("results", [])]
print(f"Filter min_price=10M max_price=15M returned prices (first 5): {prices[:5]}")

# Test filter: furnishing
_, res_furn = api_req("/v1/listings", {"furnishing": "fully-furnished"}, headers=headers)
furns = set(l.get("furnishing") for l in res_furn.get("results", []))
print(f"Filter furnishing='fully-furnished' returned furnishings: {furns}")

# Test filter: property_type
_, res_prop = api_req("/v1/listings", {"property_type": "apartment"}, headers=headers)
ptypes = set(l.get("property_type") for l in res_prop.get("results", []))
print(f"Filter property_type='apartment' returned types: {ptypes}")

# Test sorting: sort_by=price order=desc
_, res_sort_p = api_req("/v1/listings", {"sort_by": "price", "order": "desc"}, headers=headers)
sorted_prices = [l.get("price") for l in res_sort_p.get("results", [])]
is_sorted_p = (sorted_prices == sorted(sorted_prices, reverse=True))
print(f"sort_by=price order=desc: first 5 prices={sorted_prices[:5]}, Is correctly sorted? {is_sorted_p}")

# Test sorting: sort_by=carpet_area order=asc
_, res_sort_c = api_req("/v1/listings", {"sort_by": "carpet_area", "order": "asc"}, headers=headers)
sorted_carpet = [l.get("carpet_area") for l in res_sort_c.get("results", [])]
is_sorted_c = (sorted_carpet == sorted(sorted_carpet))
print(f"sort_by=carpet_area order=asc: first 5 carpet={sorted_carpet[:5]}, Is correctly sorted? {is_sorted_c}")

