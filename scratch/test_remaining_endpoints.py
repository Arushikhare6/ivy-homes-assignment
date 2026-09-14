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
headers = {"Authorization": f"Bearer {token}"}

print("=== 1. RENTALS SINGLE ITEM PATH ===")
st_r_plur, res_r_plur = api_req("/v1/rentals/R4000001", headers=headers)
print(f"GET /v1/rentals/R4000001: status {st_r_plur}")

st_r_sing, res_r_sing = api_req("/v1/rental/R4000001", headers=headers)
print(f"GET /v1/rental/R4000001: status {st_r_sing}")

print("\n=== 2. PROJECTS SINGLE ITEM PATH ===")
st_p_plur, res_p_plur = api_req("/v1/projects/P40001", headers=headers)
print(f"GET /v1/projects/P40001: status {st_p_plur}")

st_p_sing, res_p_sing = api_req("/v1/project/P40001", headers=headers)
print(f"GET /v1/project/P40001: status {st_p_sing}")

print("\n=== 3. LOGOUT ENDPOINT ===")
st_log, res_log = api_req("/auth/logout", method="POST", headers=headers)
print(f"POST /auth/logout: status {st_log} -> {res_log}")

# Check if token is invalidated after logout
st_after, res_after = api_req("/v1/listings", {"limit": 1}, headers=headers)
print(f"GET /v1/listings after logout: status {st_after} -> {res_after}")

