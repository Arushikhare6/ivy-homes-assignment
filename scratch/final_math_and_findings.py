import json
import os
import re
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict

DATA_DIR = r"C:\Users\arushi khare\.gemini\antigravity\brain\9e4ee355-335e-48a8-93dd-6b51a285a691\scratch\data"

with open(os.path.join(DATA_DIR, "listings_exact.json")) as f:
    listings = json.load(f)

with open(os.path.join(DATA_DIR, "rentals_exact.json")) as f:
    rentals = json.load(f)

with open(os.path.join(DATA_DIR, "projects_exact.json")) as f:
    projects = json.load(f)

ist = timezone(timedelta(hours=5, minutes=30))
ref_end = datetime(2026, 9, 10, 0, 0, 0, tzinfo=ist)
ref_start = ref_end - timedelta(days=7)

def parse_ist(ts_str):
    if not ts_str:
        return None
    if ts_str.endswith("Z"):
        dt = datetime.fromisoformat(ts_str[:-1] + "+00:00")
        return dt.astimezone(ist)
    try:
        dt = datetime.fromisoformat(ts_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ist)
        else:
            dt = dt.astimezone(ist)
        return dt
    except Exception:
        return None

# Q1
q1 = len(listings)

# Q2: Unique properties deduplication
prop_keys = set()
for l in listings:
    key = (
        (l.get("locality") or "").lower().strip(),
        (l.get("apartment_name") or "").lower().strip(),
        l.get("floor"),
        l.get("bedroom"),
        l.get("carpet_area"),
        l.get("super_built_up_area"),
        (l.get("facing_direction") or "").lower().strip()
    )
    prop_keys.add(key)
q2 = len(prop_keys)

# Q3
q3 = sum(1 for l in listings if l.get("is_live") is True)

# Q4: Corrupt listing IDs
corrupt_reasons = {}
corrupt_set = set()

for l in listings:
    lid = l["listing_id"]
    reasons = []

    bhk = l.get("bedroom")
    bath = l.get("bathroom")
    carpet = l.get("carpet_area")
    super_built = l.get("super_built_up_area")
    floor = l.get("floor")
    total_floors = l.get("total_floors")
    price = l.get("price")
    lat = l.get("latitude")
    lon = l.get("longitude")
    balcony = l.get("balcony")
    parking = l.get("covered_parking")
    posted_at = l.get("posted_at")

    if bhk is None or bhk <= 0:
        reasons.append(f"Invalid bedroom: {bhk}")
    if bath is None or bath <= 0:
        reasons.append(f"Invalid bathroom: {bath}")
    if carpet is None or carpet <= 0:
        reasons.append(f"Invalid carpet_area: {carpet}")
    if super_built is not None and carpet is not None and super_built > 0 and carpet > super_built:
        reasons.append(f"carpet_area ({carpet}) > super_built_up_area ({super_built})")
    if floor is not None and total_floors is not None and total_floors > 0 and floor > total_floors:
        reasons.append(f"floor ({floor}) > total_floors ({total_floors})")
    if floor is not None and floor < 0:
        reasons.append(f"Negative floor: {floor}")
    if price is None or price <= 0:
        reasons.append(f"Invalid price: {price}")
    if balcony is not None and balcony < 0:
        reasons.append(f"Negative balcony: {balcony}")
    if parking is not None and parking < 0:
        reasons.append(f"Negative parking: {parking}")
    if lat is None or lon is None or not (12.0 <= lat <= 14.0 and 79.5 <= lon <= 80.5):
        reasons.append(f"Coordinates out of bounds: ({lat}, {lon})")

    if reasons:
        corrupt_reasons[lid] = reasons
        corrupt_set.add(lid)

q4_corrupt_ids = sorted(list(corrupt_set))

# Q5: total_monthly_rent in T Nagar
t_nagar_rentals = [r for r in rentals if r.get("locality", "").lower().strip() == "t nagar"]
q5 = sum(r.get("price", 0) for r in t_nagar_rentals)

# Q9: Fake listing IDs
phone_names = defaultdict(set)
phone_listings = defaultdict(list)
for l in listings:
    p = l.get("posted_by_contact")
    phone_names[p].add(l.get("posted_by_name"))
    phone_listings[p].append(l["listing_id"])

fake_phone_set = set()
for p, names in phone_names.items():
    if len(names) > 1: # phone number used by multiple fake names
        for lid in phone_listings[p]:
            fake_phone_set.add(lid)

# Also listings with monthly rent listed as sale price (< 100,000 INR)
fake_rent_as_sale_set = set(l["listing_id"] for l in listings if 0 < l.get("price", 0) < 100000)

all_fake_set = fake_phone_set | fake_rent_as_sale_set
# Exclude any that are corrupt so corrupt and fake don't overlap if needed, or keep complete
q9_fake_ids = sorted(list(all_fake_set - set(q4_corrupt_ids)))

# Q6: avg_price_per_sqft_2bhk
eligible_2bhk_rates = []
for l in listings:
    lid = l["listing_id"]
    if l.get("is_live") is True and l.get("bedroom") == 2:
        if lid not in q4_corrupt_ids and lid not in q9_fake_ids:
            price = l.get("price", 0)
            carpet = l.get("carpet_area", 0)
            if price > 0 and carpet > 0:
                eligible_2bhk_rates.append(price / carpet)

q6 = round(sum(eligible_2bhk_rates) / len(eligible_2bhk_rates), 2) if eligible_2bhk_rates else 0.0

# Q7: costliest_project
max_p_inr = -1
costliest_proj_id = None
for p in projects:
    p_max = p.get("price_max", 0)
    if p_max < 10:
        inr_val = int(round(p_max * 10000000))
    elif p_max < 1000:
        inr_val = int(round(p_max * 100000))
    else:
        inr_val = int(p_max)
    
    if inr_val > max_p_inr:
        max_p_inr = inr_val
        costliest_proj_id = p.get("project_id")

q7 = {"project_id": costliest_proj_id, "price_max_inr": max_p_inr}

# Q8: listings_last_7_days
q8 = 0
for l in listings:
    ts = parse_ist(l.get("posted_at"))
    if ts and ref_start <= ts < ref_end:
        q8 += 1

# Q10: projects_with_wrong_listing_count
listings_per_project = Counter(l.get("project_id") for l in listings if l.get("project_id"))
q10 = 0
for p in projects:
    pid = p.get("project_id")
    reported = p.get("total_listings", 0)
    actual = listings_per_project.get(pid, 0)
    if reported != actual:
        q10 += 1

answers_dict = {
    "total_listing_records": q1,
    "unique_properties": q2,
    "active_listings": q3,
    "corrupt_listing_ids": q4_corrupt_ids,
    "total_monthly_rent": q5,
    "avg_price_per_sqft_2bhk": q6,
    "costliest_project": q7,
    "listings_last_7_days": q8,
    "fake_listing_ids": q9_fake_ids,
    "projects_with_wrong_listing_count": q10
}

print("\n==========================================")
print("FINAL CALCULATED ANSWERS")
print("==========================================")
print(json.dumps(answers_dict, indent=2))

with open(os.path.join(DATA_DIR, "calculated_answers.json"), "w") as f:
    json.dump(answers_dict, f, indent=2)

