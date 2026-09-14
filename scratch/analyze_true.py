import json
import os
import re
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict

DATA_DIR = r"C:\Users\arushi khare\.gemini\antigravity\brain\9e4ee355-335e-48a8-93dd-6b51a285a691\scratch\data"

with open(os.path.join(DATA_DIR, "listings_true.json")) as f:
    listings = json.load(f)

with open(os.path.join(DATA_DIR, "rentals_true.json")) as f:
    rentals = json.load(f)

with open(os.path.join(DATA_DIR, "projects_true.json")) as f:
    projects = json.load(f)

print(f"=== TRUE DATASETS LOADED ===")
print(f"Listings count: {len(listings)}")
print(f"Rentals count: {len(rentals)}")
print(f"Projects count: {len(projects)}")

# 1. Unique listing IDs in listings_true.json
listing_ids = [l["listing_id"] for l in listings]
id_counts = Counter(listing_ids)
print(f"\nUnique listing IDs in listings_true.json: {len(id_counts)}")
print(f"Top 5 most frequent listing_ids in listings_true.json:")
for lid, cnt in id_counts.most_common(5):
    print(f"  {lid}: {cnt} times")

# Let's check why there are duplicate IDs! Are they duplicate records returned across offset pages, or does the dataset contain exact duplicate IDs?
print(f"Number of distinct listing_ids: {len(set(listing_ids))}")

# 2. Check corrupt listing IDs in true dataset
corrupt_ids = set()
corrupt_details = {}

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
        issues.append(f"Invalid price: {price}")
    if carpet is None or carpet <= 0:
        issues.append(f"Invalid carpet_area: {carpet}")
    if super_built is not None and carpet is not None and carpet > super_built:
        issues.append(f"carpet_area ({carpet}) > super_built_up_area ({super_built})")
    if floor is not None and total_floors is not None and floor > total_floors:
        issues.append(f"floor ({floor}) > total_floors ({total_floors})")
    if floor is not None and floor < -2:
        issues.append(f"Impossible floor: {floor}")
    if bhk is None or bhk <= 0:
        issues.append(f"Invalid bedroom: {bhk}")
    if bath is None or bath <= 0:
        issues.append(f"Invalid bathroom: {bath}")
    if balcony is not None and balcony < 0:
        issues.append(f"Negative balcony: {balcony}")
    if parking is not None and parking < 0:
        issues.append(f"Negative parking: {parking}")
    if lat is None or lon is None or not (12.0 <= lat <= 14.0 and 79.5 <= lon <= 80.6):
        issues.append(f"Coordinates out of bounds: ({lat}, {lon})")

    if issues:
        corrupt_ids.add(lid)
        corrupt_details[lid] = issues

print(f"\nCorrupt listing IDs count: {len(corrupt_ids)}")
print(f"Sorted corrupt listing IDs: {sorted(list(corrupt_ids))}")
for lid in sorted(list(corrupt_ids)):
    print(f"  {lid}: {'; '.join(corrupt_details[lid])}")

# 3. Check fake listing IDs in true dataset
# Fake listings analysis:
# Look for fake phone numbers, copy-pasted descriptions across distinct properties, suspicious titles, domain URLs, fake patterns.
fake_ids = set()

# Group by contact number
contact_to_listings = defaultdict(list)
for l in listings:
    c = l.get("posted_by_contact")
    contact_to_listings[c].append(l)

print("\n--- Phone number analysis ---")
for contact, l_list in sorted(contact_to_listings.items(), key=lambda x: len(x[1]), reverse=True):
    unique_locs = set(l.get("locality") for l in l_list)
    unique_names = set(l.get("posted_by_name") for l in l_list)
    unique_types = set(l.get("property_type") for l in l_list)
    print(f"Contact {contact}: {len(l_list)} records across {len(unique_locs)} localities. Names: {unique_names}")
    
    # Check if contact is suspicious: e.g. same contact used with different agent names or 100+ listings across 20 localities
    if len(l_list) > 50 or len(unique_names) > 1:
        for l in l_list:
            # Check if this contact has fake/scam behavior
            pass

# Check URL domains and validity
urls = [l.get("listing_url") for l in listings]
url_domains = Counter(u.split("/")[2] if u and "/" in u else "invalid" for u in urls)
print(f"\nListing URL domains: {dict(url_domains)}")

# Check description text patterns
desc_counts = Counter(l.get("description") for l in listings)
print(f"\nTop 5 duplicate descriptions count:")
for d, cnt in desc_counts.most_common(5):
    print(f"  '{d[:60]}...': {cnt} times")

