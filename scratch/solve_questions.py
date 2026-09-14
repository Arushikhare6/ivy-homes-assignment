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

print(f"Loaded exact datasets: {len(listings)} listings, {len(rentals)} rentals, {len(projects)} projects.")

# IST timezone setup
ist = timezone(timedelta(hours=5, minutes=30))
ref_end = datetime(2026, 9, 10, 0, 0, 0, tzinfo=ist)
ref_start = ref_end - timedelta(days=7)

def parse_ist(ts_str):
    if not ts_str:
        return None
    # If ends with Z, convert from UTC to IST
    if ts_str.endswith("Z"):
        dt = datetime.fromisoformat(ts_str[:-1] + "+00:00")
        return dt.astimezone(ist)
    # If string has offset, convert to IST
    try:
        dt = datetime.fromisoformat(ts_str)
        if dt.tzinfo is None:
            # Naive timestamp - assume UTC or IST? Let's check API health timezone (Asia/Kolkata +05:30)
            # If server local time is IST, naive ISO string is IST.
            dt = dt.replace(tzinfo=ist)
        else:
            dt = dt.astimezone(ist)
        return dt
    except Exception:
        return None

# =============================================================
# Q1: total_listing_records
# =============================================================
q1_total_listing_records = len(listings)

# =============================================================
# Q3: active_listings
# =============================================================
q3_active_listings = sum(1 for l in listings if l.get("is_live") is True)

# =============================================================
# Q4: corrupt_listing_ids
# =============================================================
corrupt_reasons = {}
corrupt_ids = []

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
    if lat is None or lon is None or not (12.5 <= lat <= 13.5 and 79.8 <= lon <= 80.5):
        reasons.append(f"Coordinates outside Chennai bounds: ({lat}, {lon})")

    if reasons:
        corrupt_reasons[lid] = reasons
        corrupt_ids.append(lid)

corrupt_ids = sorted(list(set(corrupt_ids)))

# =============================================================
# Q5: total_monthly_rent (T Nagar)
# =============================================================
t_nagar_rentals = [r for r in rentals if r.get("locality", "").lower().strip() == "t nagar"]
q5_total_monthly_rent = sum(r.get("price", 0) for r in t_nagar_rentals)

# =============================================================
# Q8: listings_last_7_days
# =============================================================
q8_recent_count = 0
for l in listings:
    ts = parse_ist(l.get("posted_at"))
    if ts and ref_start <= ts < ref_end:
        q8_recent_count += 1

# =============================================================
# Q10: projects_with_wrong_listing_count
# =============================================================
listings_per_project = Counter(l.get("project_id") for l in listings if l.get("project_id"))
q10_wrong_count = 0
project_diffs = []

for p in projects:
    pid = p.get("project_id")
    reported = p.get("total_listings", 0)
    actual = listings_per_project.get(pid, 0)
    if reported != actual:
        q10_wrong_count += 1
        project_diffs.append((pid, p.get("apartment_name"), reported, actual))

# =============================================================
# Q7: costliest_project
# =============================================================
# Standardizing project price_max to INR:
# In projects_exact.json, price_min and price_max are given in Lakhs (or Crores if >= 1).
# Let's inspect price_max format for all projects.
costliest_proj_obj = None
max_price_inr = -1

for p in projects:
    p_max = p.get("price_max", 0)
    # Convert to INR:
    # If p_max >= 1 and < 100, e.g. 93.7 -> 93.7 Lakhs = 9,370,000 INR or 93.7 Crores?
    # Let's check: 93.7 Lakhs = 9,370,000 INR (93.7 * 100000).
    # If p_max is e.g. 1.95 -> 1.95 Crores = 19,500,000 INR (1.95 * 10000000).
    # Let's write logic to parse price_max exact INR value!
    if p_max < 10: # Crores
        inr_val = int(round(p_max * 10000000))
    elif p_max < 1000: # Lakhs
        inr_val = int(round(p_max * 100000))
    else: # Already in INR
        inr_val = int(p_max)
    
    if inr_val > max_price_inr:
        max_price_inr = inr_val
        costliest_proj_obj = {
            "project_id": p.get("project_id"),
            "price_max_inr": inr_val,
            "raw_price_max": p_max,
            "apartment_name": p.get("apartment_name")
        }

# =============================================================
# Q9: fake_listing_ids (Detailed detection)
# =============================================================
# Let's analyze suspicious features across listings to detect fake listings
fake_ids = set()
fake_reasons = defaultdict(list)

# Check duplicate physical listings posted under fake contacts or fake URLs
# Group listings by exact physical property: (locality, apartment_name, floor, bedroom, carpet_area)
prop_clusters = defaultdict(list)
for l in listings:
    key = (
        (l.get("locality") or "").lower().strip(),
        (l.get("apartment_name") or "").lower().strip(),
        l.get("floor"),
        l.get("bedroom"),
        l.get("carpet_area")
    )
    prop_clusters[key].append(l)

# Check contacts operating scam/lead-gen
contact_counts = Counter(l.get("posted_by_contact") for l in listings)
scam_contacts = set(c for c, cnt in contact_counts.items() if cnt > 50)

for l in listings:
    lid = l["listing_id"]
    contact = l.get("posted_by_contact")
    url = l.get("listing_url") or ""
    desc = l.get("description") or ""

    # Rule A: Posted by known lead-gen / scam phone numbers operating > 50 fake listings
    if contact in scam_contacts:
        fake_ids.add(lid)
        fake_reasons[lid].append(f"High-frequency lead-gen contact: {contact}")

    # Rule B: Fake URL pattern or domain
    if "fake" in url or "test" in url or "dummy" in url:
        fake_ids.add(lid)
        fake_reasons[lid].append(f"Fake URL: {url}")

    # Rule C: Description containing fake / lead keywords
    if re.search(r"\b(fake|lead gen|sample|dummy|test listing|inquiry only)\b", desc, re.IGNORECASE):
        fake_ids.add(lid)
        fake_reasons[lid].append(f"Fake keyword in description")

fake_ids = sorted(list(fake_ids))

# =============================================================
# Q6: avg_price_per_sqft_2bhk
# =============================================================
# Eligible listings: is_live == True, bedroom == 2, not in corrupt_ids, not in fake_ids
eligible_rates = []
for l in listings:
    lid = l["listing_id"]
    if l.get("is_live") is True and l.get("bedroom") == 2:
        if lid not in corrupt_ids and lid not in fake_ids:
            price = l.get("price", 0)
            carpet = l.get("carpet_area", 0)
            if price > 0 and carpet > 0:
                rate = price / carpet
                eligible_rates.append(rate)

q6_avg_rate = round(sum(eligible_rates) / len(eligible_rates), 2) if eligible_rates else 0.0

# Print complete summary
print("\n==========================================")
print("PRELIMINARY ANSWERS SUMMARY")
print("==========================================")
print(f"1. total_listing_records: {q1_total_listing_records}")
print(f"2. unique_properties (clusters count): {len(prop_clusters)}")
print(f"3. active_listings: {q3_active_listings}")
print(f"4. corrupt_listing_ids ({len(corrupt_ids)}): {corrupt_ids}")
print(f"5. total_monthly_rent (T Nagar): {q5_total_monthly_rent}")
print(f"6. avg_price_per_sqft_2bhk: {q6_avg_rate} (based on {len(eligible_rates)} eligible 2BHK listings)")
print(f"7. costliest_project: {costliest_proj_obj}")
print(f"8. listings_last_7_days: {q8_recent_count}")
print(f"9. fake_listing_ids ({len(fake_ids)}): {fake_ids[:10]} ... (total {len(fake_ids)})")
print(f"10. projects_with_wrong_listing_count: {q10_wrong_count} / {len(projects)}")

