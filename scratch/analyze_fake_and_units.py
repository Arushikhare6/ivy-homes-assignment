import json
import os
from collections import Counter, defaultdict

DATA_DIR = r"C:\Users\arushi khare\.gemini\antigravity\brain\9e4ee355-335e-48a8-93dd-6b51a285a691\scratch\data"

with open(os.path.join(DATA_DIR, "listings_exact.json")) as f:
    listings = json.load(f)

print(f"Total listings: {len(listings)}")

# 1. Price analysis: listings with price < 1,000,000 (10 Lakhs)
low_price_listings = [l for l in listings if l.get("price", 0) < 1000000]
print(f"\nListings with price < 10 Lakhs (1,000,000 INR): {len(low_price_listings)}")
for l in low_price_listings[:10]:
    print(f"  {l['listing_id']} ({l['locality']}): price={l['price']}, carpet={l['carpet_area']}, bhk={l['bedroom']}, contact={l['posted_by_contact']}")
    print(f"     desc: {l.get('description')[:70]}")

# 2. Check if phone numbers with multiple names are lead-gen / fake listings
phone_names = defaultdict(set)
phone_listings = defaultdict(list)
for l in listings:
    p = l.get("posted_by_contact")
    phone_names[p].add(l.get("posted_by_name"))
    phone_listings[p].append(l["listing_id"])

mismatched_phones = {p: names for p, names in phone_names.items() if len(names) > 1}
fake_phone_listing_ids = []
for p in mismatched_phones:
    fake_phone_listing_ids.extend(phone_listings[p])

fake_phone_listing_ids = sorted(list(set(fake_phone_listing_ids)))
print(f"\nListings associated with multi-identity/scam phone numbers: {len(fake_phone_listing_ids)}")

# 3. Check listings where price is in Thousands (e.g. price < 100,000)
rental_price_sale_listings = [l["listing_id"] for l in listings if l.get("price", 0) < 100000]
print(f"Listings where price < 100,000 (monthly rent put as sale price): {len(rental_price_sale_listings)}")

# 4. Combine all fake listing candidates
all_fake_candidates = sorted(list(set(fake_phone_listing_ids + rental_price_sale_listings)))
print(f"\nTotal Candidate Fake Listings: {len(all_fake_candidates)}")

