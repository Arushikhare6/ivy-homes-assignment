import json
import os
import statistics
from collections import defaultdict

DATA_DIR = r"C:\Users\arushi khare\.gemini\antigravity\brain\9e4ee355-335e-48a8-93dd-6b51a285a691\scratch\data"

with open(os.path.join(DATA_DIR, "listings_exact.json")) as f:
    listings = json.load(f)

# Filter active live listings with positive price and carpet area
active_listings = [l for l in listings if l.get("is_live") is True and l.get("price", 0) > 0 and l.get("carpet_area", 0) > 0]

prices = [l["price"] for l in active_listings]
rates = [l["price"] / l["carpet_area"] for l in active_listings]

median_price = statistics.median(prices) if prices else 0
median_price_per_sqft = statistics.median(rates) if rates else 0

# By Locality
locality_groups = defaultdict(list)
for l in active_listings:
    loc = (l.get("locality") or "unknown").lower().strip()
    locality_groups[loc].append(l)

by_locality = []
for loc, loc_list in sorted(locality_groups.items(), key=lambda x: len(x[1]), reverse=True):
    loc_prices = [l["price"] for l in loc_list]
    by_locality.append({
        "locality": loc,
        "count": len(loc_list),
        "median_price": int(statistics.median(loc_prices))
    })

# By BHK
bhk_groups = defaultdict(list)
for l in active_listings:
    bhk = l.get("bedroom", 0)
    bhk_groups[bhk].append(l)

by_bhk = []
for bhk, bhk_list in sorted(bhk_groups.items()):
    bhk_prices = [l["price"] for l in bhk_list]
    by_bhk.append({
        "bedroom": bhk,
        "count": len(bhk_list),
        "median_price": int(statistics.median(bhk_prices))
    })

summary_res = {
    "city": "chennai",
    "total_listings": len(active_listings),
    "total_records_retrieved": len(listings),
    "median_price": int(median_price),
    "median_price_per_sqft": int(round(median_price_per_sqft)),
    "by_locality": by_locality,
    "by_bhk": by_bhk
}

print(json.dumps(summary_res, indent=2))

with open(os.path.join(DATA_DIR, "analytics_summary_computed.json"), "w") as f:
    json.dump(summary_res, f, indent=2)

