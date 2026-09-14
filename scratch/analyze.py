import json
import os
import re
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict

DATA_DIR = r"C:\Users\arushi khare\.gemini\antigravity\brain\9e4ee355-335e-48a8-93dd-6b51a285a691\scratch\data"

with open(os.path.join(DATA_DIR, "listings.json")) as f:
    listings = json.load(f)

with open(os.path.join(DATA_DIR, "rentals.json")) as f:
    rentals = json.load(f)

with open(os.path.join(DATA_DIR, "projects.json")) as f:
    projects = json.load(f)

print(f"Loaded {len(listings)} listings, {len(rentals)} rentals, {len(projects)} projects.")

# Inspect listing fields and types
sample_listing = listings[0]
print("\n--- SAMPLE LISTING ---")
print(json.dumps(sample_listing, indent=2))

sample_rental = rentals[0]
print("\n--- SAMPLE RENTAL ---")
print(json.dumps(sample_rental, indent=2))

sample_project = projects[0]
print("\n--- SAMPLE PROJECT ---")
print(json.dumps(sample_project, indent=2))

# -------------------------------------------------------------
# Question 1: Total listing records retrievable
# -------------------------------------------------------------
print("\n=== QUESTION 1: Total Listing Records ===")
print(f"Total retrieved listing records: {len(listings)}")

# -------------------------------------------------------------
# Question 3: Active listings (is_live == True)
# -------------------------------------------------------------
print("\n=== QUESTION 3: Active Listings ===")
is_live_counts = Counter(l.get("is_live") for l in listings)
print(f"is_live value counts: {dict(is_live_counts)}")

# -------------------------------------------------------------
# Question 4: Corrupt listing IDs
# -------------------------------------------------------------
print("\n=== QUESTION 4: Corrupt Listing IDs ===")
corrupt_reasons = defaultdict(list)

for l in listings:
    lid = l["listing_id"]
    price = l.get("price")
    carpet = l.get("carpet_area")
    super_built = l.get("super_built_up_area")
    floor = l.get("floor")
    total_floors = l.get("total_floors")
    bhk = l.get("bedroom")
    bath = l.get("bathroom")
    lat = l.get("latitude")
    lon = l.get("longitude")

    # Check anomalies
    if price is not None and price <= 0:
        corrupt_reasons[lid].append(f"Invalid price: {price}")
    if carpet is not None and carpet <= 0:
        corrupt_reasons[lid].append(f"Invalid carpet_area: {carpet}")
    if super_built is not None and carpet is not None and super_built > 0 and carpet > super_built:
        corrupt_reasons[lid].append(f"carpet_area ({carpet}) > super_built_up_area ({super_built})")
    if floor is not None and total_floors is not None and total_floors > 0 and floor > total_floors:
        corrupt_reasons[lid].append(f"floor ({floor}) > total_floors ({total_floors})")
    if floor is not None and floor < -2: # basement -1, -2 can be okay, lower is impossible
        corrupt_reasons[lid].append(f"Impossible floor: {floor}")
    if bhk is not None and bhk <= 0:
        corrupt_reasons[lid].append(f"Invalid bedroom: {bhk}")
    if bath is not None and bath < 0:
        corrupt_reasons[lid].append(f"Invalid bathroom: {bath}")
    if lat is not None and lon is not None:
        # Chennai bounding box: lat ~ 12.8 to 13.3, lon ~ 80.0 to 80.4
        if not (12.0 <= lat <= 14.0 and 79.5 <= lon <= 80.6):
            corrupt_reasons[lid].append(f"Coordinates outside Chennai area: ({lat}, {lon})")

print(f"Found {len(corrupt_reasons)} corrupt listings:")
for lid, reasons in sorted(corrupt_reasons.items())[:20]:
    print(f"  {lid}: {', '.join(reasons)}")

# -------------------------------------------------------------
# Question 5: Total monthly rent in assigned locality (T Nagar)
# -------------------------------------------------------------
print("\n=== QUESTION 5: Total Monthly Rent in T Nagar ===")
t_nagar_rentals = [r for r in rentals if r.get("locality", "").lower() == "t nagar"]
print(f"Count of rentals in T Nagar: {len(t_nagar_rentals)}")
total_rent_t_nagar = sum(r.get("price", 0) for r in t_nagar_rentals)
print(f"Total monthly rent sum: {total_rent_t_nagar}")
for r in t_nagar_rentals[:5]:
    print(f"  {r['listing_id']} - {r['apartment_name']} - locality: {r['locality']} - price: {r['price']}")

# -------------------------------------------------------------
# Question 7: Costliest project
# -------------------------------------------------------------
print("\n=== QUESTION 7: Costliest Project ===")
costliest = max(projects, key=lambda p: p.get("price_max", p.get("price_max_inr", 0)))
print(f"Costliest project raw object: {json.dumps(costliest, indent=2)}")

# -------------------------------------------------------------
# Question 8: Listings in last 7 days
# Reference = 2026-09-10T00:00:00+05:30 (IST)
# Range = [2026-09-03T00:00:00+05:30, 2026-09-10T00:00:00+05:30)
# -------------------------------------------------------------
print("\n=== QUESTION 8: Listings in Last 7 Days ===")

ist = timezone(timedelta(hours=5, minutes=30))
ref_end = datetime(2026, 9, 10, 0, 0, 0, tzinfo=ist)
ref_start = ref_end - timedelta(days=7)

def parse_iso(ts_str):
    if not ts_str:
        return None
    # Replace Z with +00:00
    if ts_str.endswith("Z"):
        ts_str = ts_str[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(ts_str)
        return dt.astimezone(ist)
    except Exception as e:
        return None

recent_count = 0
invalid_ts_count = 0
posted_dates = []

for l in listings:
    ts = parse_iso(l.get("posted_at"))
    if ts is None:
        invalid_ts_count += 1
    else:
        posted_dates.append(ts)
        if ref_start <= ts < ref_end:
            recent_count += 1

print(f"Listings posted in [2026-09-03, 2026-09-10 IST): {recent_count}")
print(f"Listings with invalid/unparseable timestamps: {invalid_ts_count}")

# -------------------------------------------------------------
# Question 10: Projects with wrong listing count
# -------------------------------------------------------------
print("\n=== QUESTION 10: Projects with wrong listing count ===")
listings_per_project = Counter(l.get("project_id") for l in listings if l.get("project_id"))

mismatched_projects = 0
for p in projects:
    pid = p.get("project_id")
    reported = p.get("total_listings", 0)
    actual = listings_per_project.get(pid, 0)
    if reported != actual:
        mismatched_projects += 1

print(f"Total projects: {len(projects)}")
print(f"Projects with mismatched listing count: {mismatched_projects}")

