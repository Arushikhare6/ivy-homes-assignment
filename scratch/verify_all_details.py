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

print(f"Loaded datasets: {len(listings)} listings, {len(rentals)} rentals, {len(projects)} projects.")

# -------------------------------------------------------------
# FAKE LISTINGS DEEP DIVE
# -------------------------------------------------------------
print("\n==========================================")
print("INVESTIGATING FAKE LISTINGS PATTERNS")
print("==========================================")

# Let's inspect phone numbers
phone_counts = Counter(l.get("posted_by_contact") for l in listings)
print(f"Top 10 most common phone numbers in listings:")
for p, c in phone_counts.most_common(10):
    sample = [l for l in listings if l.get("posted_by_contact") == p][0]
    print(f"  {p}: {c} listings. Sample name: {sample.get('posted_by_name')}, role: {sample.get('posted_by')}")

# Check if phone numbers have multiple DIFFERENT names
phone_names = defaultdict(set)
for l in listings:
    phone_names[l.get("posted_by_contact")].add(l.get("posted_by_name"))

mismatched_phone_names = {p: names for p, names in phone_names.items() if len(names) > 1}
print(f"\nPhone numbers with multiple names ({len(mismatched_phone_names)}):")
for p, names in list(mismatched_phone_names.items())[:10]:
    print(f"  {p}: {names}")

# Check duplicate descriptions across different apartment names or localities
desc_locations = defaultdict(set)
desc_listings = defaultdict(list)
for l in listings:
    d = (l.get("description") or "").strip()
    if d:
        desc_locations[d].add((l.get("locality"), l.get("apartment_name")))
        desc_listings[d].append(l["listing_id"])

suspicious_desc = {d: locs for d, locs in desc_locations.items() if len(locs) > 1}
print(f"\nDescriptions reused across multiple distinct properties/localities ({len(suspicious_desc)}):")
for d, locs in list(suspicious_desc.items())[:10]:
    print(f"  Desc: '{d[:70]}...' -> {len(locs)} different property/locality combos ({len(desc_listings[d])} listings)")

# Check price vs carpet area outliers (price per sqft)
rates = []
for l in listings:
    p = l.get("price", 0)
    c = l.get("carpet_area", 0)
    if p > 0 and c > 0:
        rates.append((p / c, l))

rates.sort(key=lambda x: x[0])
print(f"\nLowest 5 price/sqft listings:")
for r, l in rates[:5]:
    print(f"  {l['listing_id']} ({l['locality']}): rate={r:.2f} Rs/sqft, price={l['price']}, carpet={l['carpet_area']}, contact={l['posted_by_contact']}")
    print(f"     desc: {l.get('description')[:70]}")

print(f"\nHighest 5 price/sqft listings:")
for r, l in rates[-5:]:
    print(f"  {l['listing_id']} ({l['locality']}): rate={r:.2f} Rs/sqft, price={l['price']}, carpet={l['carpet_area']}, contact={l['posted_by_contact']}")
    print(f"     desc: {l.get('description')[:70]}")

# Check website / URL discrepancies or fake URLs
url_websites = defaultdict(set)
for l in listings:
    w = l.get("website")
    u = l.get("listing_url", "")
    url_websites[w].add(u.split("/")[2] if "/" in u else u)

print(f"\nWebsite vs domain mapping:")
for w, doms in url_websites.items():
    print(f"  Website '{w}': domains {doms}")

# Check `posted_by` values
posted_by_counts = Counter(l.get("posted_by") for l in listings)
print(f"\nposted_by counts: {dict(posted_by_counts)}")

# Check `is_verified` vs fake
verified_counts = Counter(l.get("is_verified") for l in listings)
print(f"\nis_verified counts: {dict(verified_counts)}")

