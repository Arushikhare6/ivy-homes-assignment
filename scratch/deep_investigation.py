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

# -------------------------------------------------------------
# 1. CORRUPT LISTINGS ANALYSIS
# -------------------------------------------------------------
print("\n==========================================")
print("1. DETAILED CORRUPT LISTINGS ANALYSIS")
print("==========================================")

corrupt_dict = {}

for l in listings:
    lid = l["listing_id"]
    issues = []

    price = l.get("price")
    carpet = l.get("carpet_area")
    super_built = l.get("super_built_up_area")
    floor = l.get("floor")
    total_floors = l.get("total_floors")
    bhk = l.get("bedroom")
    bath = l.get("bathroom")
    lat = l.get("latitude")
    lon = l.get("longitude")
    balcony = l.get("balcony")
    parking = l.get("covered_parking")
    posted_at = l.get("posted_at")

    if price is None or price <= 0:
        issues.append(f"Price <= 0: {price}")
    if carpet is None or carpet <= 0:
        issues.append(f"Carpet area <= 0: {carpet}")
    if super_built is not None and carpet is not None and carpet > super_built:
        issues.append(f"Carpet ({carpet}) > SuperBuilt ({super_built})")
    if floor is not None and total_floors is not None and floor > total_floors:
        issues.append(f"Floor ({floor}) > TotalFloors ({total_floors})")
    if floor is not None and floor < 0:
        issues.append(f"Negative floor: {floor}")
    if bhk is None or bhk <= 0:
        issues.append(f"Bedroom <= 0: {bhk}")
    if bath is None or bath <= 0:
        issues.append(f"Bathroom <= 0: {bath}")
    if balcony is not None and balcony < 0:
        issues.append(f"Negative balcony: {balcony}")
    if parking is not None and parking < 0:
        issues.append(f"Negative parking: {parking}")

    # Lat / lon check for Chennai
    if lat is None or lon is None or not (12.5 <= lat <= 13.5 and 79.8 <= lon <= 80.5):
        issues.append(f"Coordinates out of bounds: lat={lat}, lon={lon}")

    # Check timestamps
    if posted_at:
        try:
            ts = datetime.fromisoformat(posted_at.replace("Z", "+00:00"))
            if ts.year > 2026 or (ts.year == 2026 and ts.month > 9) or (ts.year == 2026 and ts.month == 9 and ts.day > 10):
                issues.append(f"Future posted_at: {posted_at}")
        except Exception:
            issues.append(f"Unparseable posted_at: {posted_at}")

    if issues:
        corrupt_dict[lid] = issues

print(f"Total Corrupt Listings Found: {len(corrupt_dict)}")
for lid, issues in sorted(corrupt_dict.items()):
    print(f"  {lid}: {'; '.join(issues)}")

# -------------------------------------------------------------
# 2. FAKE / LEAD-GEN LISTINGS ANALYSIS
# -------------------------------------------------------------
print("\n==========================================")
print("2. DETAILED FAKE / LEAD-GEN LISTINGS ANALYSIS")
print("==========================================")

# Let's check distribution of posted_by_contact, description, prices, websites, etc.
contact_counts = Counter(l.get("posted_by_contact") for l in listings)
desc_counts = Counter(l.get("description") for l in listings)
url_counts = Counter(l.get("listing_url") for l in listings)

print(f"Top 10 phone numbers count:")
for phone, cnt in contact_counts.most_common(10):
    print(f"  {phone}: {cnt} listings")

# Check suspicious descriptions or suspicious price/sqft
price_sqft_list = []
for l in listings:
    price = l.get("price", 0)
    carpet = l.get("carpet_area", 0)
    if price > 0 and carpet > 0:
        rate = price / carpet
        price_sqft_list.append((rate, l["listing_id"], l.get("locality"), price, carpet, l.get("posted_by_contact"), l.get("description")))

price_sqft_list.sort(key=lambda x: x[0])

print("\nLowest 10 price/sqft listings:")
for rate, lid, loc, price, carpet, contact, desc in price_sqft_list[:10]:
    print(f"  {lid} ({loc}): rate={rate:.2f} Rs/sqft, price={price}, carpet={carpet}, contact={contact}")
    print(f"     desc: {desc[:80]}")

print("\nHighest 10 price/sqft listings:")
for rate, lid, loc, price, carpet, contact, desc in price_sqft_list[-10:]:
    print(f"  {lid} ({loc}): rate={rate:.2f} Rs/sqft, price={price}, carpet={carpet}, contact={contact}")
    print(f"     desc: {desc[:80]}")

# Let's inspect phone numbers that appear across different localities or have scam text
contact_localities = defaultdict(set)
contact_listings = defaultdict(list)
for l in listings:
    c = l.get("posted_by_contact")
    contact_localities[c].add(l.get("locality"))
    contact_listings[c].append(l)

print("\nContacts operating across > 5 different localities:")
for c, locs in contact_localities.items():
    if len(locs) > 5:
        print(f"  Contact {c}: {len(locs)} localities, {len(contact_listings[c])} listings. Name: {contact_listings[c][0].get('posted_by_name')}")

# Check keywords in description
fake_keywords = ["fake", "lead", "dummy", "test", "inquiry", "scam", "duplicate", "sample", "demo", "spam"]
keyword_matches = defaultdict(list)
for l in listings:
    desc = (l.get("description") or "").lower()
    name = (l.get("posted_by_name") or "").lower()
    for kw in fake_keywords:
        if kw in desc or kw in name:
            keyword_matches[kw].append(l["listing_id"])

print(f"\nKeyword matches in listings: {dict((k, len(v)) for k, v in keyword_matches.items())}")

# -------------------------------------------------------------
# 3. UNIQUE PROPERTIES ANALYSIS
# -------------------------------------------------------------
print("\n==========================================")
print("3. UNIQUE PROPERTIES DEDUPLICATION ANALYSIS")
print("==========================================")

# A property physically exists at a location (latitude, longitude, floor, carpet_area, bedroom)
# Or (apartment_name, locality, floor, bedroom, carpet_area, facing_direction)
prop_key_1 = set() # (apartment_name, locality, floor, bedroom, carpet_area, facing_direction)
prop_key_2 = set() # (round(latitude,4), round(longitude,4), floor, bedroom, carpet_area)
prop_key_3 = set() # (locality, apartment_name, bedroom, bathroom, floor, total_floors, carpet_area, super_built_up_area)

for l in listings:
    k1 = (
        (l.get("apartment_name") or "").lower().strip(),
        (l.get("locality") or "").lower().strip(),
        l.get("floor"),
        l.get("bedroom"),
        l.get("carpet_area"),
        (l.get("facing_direction") or "").lower().strip()
    )
    prop_key_1.add(k1)

    k2 = (
        round(l.get("latitude", 0), 4),
        round(l.get("longitude", 0), 4),
        l.get("floor"),
        l.get("bedroom"),
        l.get("carpet_area")
    )
    prop_key_2.add(k2)

    k3 = (
        (l.get("locality") or "").lower().strip(),
        (l.get("apartment_name") or "").lower().strip(),
        l.get("bedroom"),
        l.get("bathroom"),
        l.get("floor"),
        l.get("total_floors"),
        l.get("carpet_area"),
        l.get("super_built_up_area")
    )
    prop_key_3.add(k3)

print(f"Total listings: {len(listings)}")
print(f"Unique property key 1 count: {len(prop_key_1)}")
print(f"Unique property key 2 count: {len(prop_key_2)}")
print(f"Unique property key 3 count: {len(prop_key_3)}")

# -------------------------------------------------------------
# 4. COSTLIEST PROJECT IN DETAIL
# -------------------------------------------------------------
print("\n==========================================")
print("4. COSTLIEST PROJECT ANALYSIS")
print("==========================================")

def parse_project_max_price_inr(p):
    p_max = p.get("price_max", 0)
    # Check if price_max is in Crores or Lakhs or Rupees
    # e.g., if p_max < 100, it's in Crores (1 Cr = 10,000,000 INR) or Lakhs (1 Lakh = 100,000 INR)?
    # Let's inspect all project prices to see the distribution!
    return p_max

project_prices = []
for p in projects:
    p_max = p.get("price_max", 0)
    p_min = p.get("price_min", 0)
    
    # Standardize to INR:
    # If p_max is e.g. 93.7 -> is that 93.7 Lakhs (9,370,000) or 93.7 Crores?
    # Let's check listing prices in the same locality/project!
    pid = p.get("project_id")
    p_listings = [l for l in listings if l.get("project_id") == pid]
    l_prices = [l.get("price", 0) for l in p_listings if l.get("price")]
    
    project_prices.append({
        "project_id": pid,
        "apartment_name": p.get("apartment_name"),
        "locality": p.get("locality"),
        "raw_price_min": p_min,
        "raw_price_max": p_max,
        "sample_listing_prices": l_prices[:3]
    })

print("Sample top 10 projects by raw_price_max:")
project_prices.sort(key=lambda x: x["raw_price_max"], reverse=True)
for pp in project_prices[:10]:
    print(f"  {pp['project_id']} ({pp['apartment_name']}, {pp['locality']}): min={pp['raw_price_min']}, max={pp['raw_price_max']}, sample_listings_inr={pp['sample_listing_prices']}")

