import json
import os

DATA_DIR = r"C:\Users\arushi khare\.gemini\antigravity\brain\9e4ee355-335e-48a8-93dd-6b51a285a691\scratch\data"
TARGET_FILE = r"c:\Users\arushi khare\OneDrive\Desktop\Ivy Homes\submission.json"

with open(os.path.join(DATA_DIR, "calculated_answers.json")) as f:
    answers = json.load(f)

findings = [
  {
    "endpoint": "*",
    "category": "auth",
    "documented": "Every request must carry the API key as a query parameter: GET /v1/listings?api_key=IVY26-XXXXXXXXXXXX.",
    "actual": "Passing api_key as a query parameter returns HTTP 401 with detail 'send your key in the X-API-Key request header, not as a query parameter'. Key must be passed in X-API-Key request header.",
    "how_found": "Called endpoints with api_key query parameter and inspected HTTP 401 error response body.",
    "impact": "All API requests formatted per documentation fail with HTTP 401 Unauthorized.",
    "evidence": []
  },
  {
    "endpoint": "/auth/login",
    "category": "auth",
    "documented": "Returns token object with field 'token', 'expires_in': 86400 (24h), user object with email and name, and states no refresh flow exists.",
    "actual": "Returns access token under field name 'access_token', expires_in is 900 seconds (15 minutes), user object lacks 'name', and response includes 'refresh_token' and 'refresh_url': '/auth/refresh'.",
    "how_found": "Executed POST /auth/login with demo credentials and inspected JSON response structure.",
    "impact": "Frontend looking for data.token or expecting 24-hour expiration fails to authenticate and fails to refresh expiring sessions.",
    "evidence": []
  },
  {
    "endpoint": "/auth/logout",
    "category": "auth",
    "documented": "Invalidates the current token server side.",
    "actual": "Does not invalidate token server-side; returns note that tokens are stateless JWTs and must be discarded client-side. Issued bearer token remains valid for API requests after logout.",
    "how_found": "Called POST /auth/logout and then successfully made authenticated requests using the logged-out token.",
    "impact": "Security vulnerability if applications rely on server-side token revocation upon user logout.",
    "evidence": []
  },
  {
    "endpoint": "/v1/listings",
    "category": "pagination",
    "documented": "Every collection endpoint takes page (1-indexed, default 1) and limit (default 20, max 200). Collection responses include page_size.",
    "actual": "The page query parameter is quietly ignored by the server. Pagination requires offset parameter (0-indexed record offset). Page limit is hard-capped at 50, and page_size is null in metadata.",
    "how_found": "Tested page=1 vs page=2 and received identical results; tested offset=50 and received the second page of results.",
    "impact": "Page-based navigation fails to fetch subsequent pages unless offset parameter is used.",
    "evidence": []
  },
  {
    "endpoint": "/v1/listings",
    "category": "completeness",
    "documented": "Response metadata total reports 3967 total listings.",
    "actual": "Response metadata total reports 3967 listings, but paging via offset to the end retrieves 4100 records in total.",
    "how_found": "Paged past reported total 3967 until results array became empty at offset 4100.",
    "impact": "Client applications stopping at reported total miss 133 valid listing records.",
    "evidence": []
  },
  {
    "endpoint": "/v1/projects",
    "category": "units",
    "documented": "price_min and price_max are in rupees as integers.",
    "actual": "price_min and price_max are floating-point numbers expressed in Lakhs (or Crores when >= 1.0), e.g. 67.7 represents 67.7 Lakhs (6,770,000 INR) and 3.78 represents 3.78 Crores (37,800,000 INR).",
    "how_found": "Inspected price_min and price_max values across /v1/projects and compared against actual listing prices.",
    "impact": "Project prices rendered directly to users appear off by a factor of 100,000 or 10,000,000.",
    "evidence": ["P40001", "P40035", "P40224", "P40005"]
  },
  {
    "endpoint": "/v1/listings",
    "category": "filters",
    "documented": "Returns active sale listings in your city. Inactive, expired and withdrawn listings are excluded server side.",
    "actual": "Returns both active and inactive/withdrawn listings. 867 of 4100 retrievable listings have is_live set to false.",
    "how_found": "Inspected is_live boolean field across all retrieved records from /v1/listings.",
    "impact": "App displaying raw records shows inactive and withdrawn properties to users unless frontend filters by is_live === true.",
    "evidence": ["ZER-4000021", "DWE-4000745", "100-4001961", "SQU-4002483", "MAG-4000870"]
  },
  {
    "endpoint": "/v1/listings",
    "category": "timestamps",
    "documented": "Timestamps are ISO 8601, UTC, Z suffix, everywhere in the API.",
    "actual": "posted_at timestamps in /v1/listings lack the Z suffix and timezone offset (e.g. '2026-01-19T12:56:00').",
    "how_found": "Parsed posted_at field across listing records.",
    "impact": "Date parsers assuming UTC offset with missing Z suffix may misinterpret local IST time as UTC.",
    "evidence": ["MAG-4001518", "100-4000035", "DWE-4001305", "SQU-4003992"]
  },
  {
    "endpoint": "/v1/listings",
    "category": "data_quality",
    "documented": "All listing attributes describe physical properties.",
    "actual": "Contains corrupt records with physically impossible data such as negative prices, bedroom = 0, carpet_area > super_built_up_area, or floor > total_floors.",
    "how_found": "Audited field constraints across all 4100 listing records.",
    "impact": "Displays impossible property data (e.g. 0 bedrooms, negative price) on listing detail pages.",
    "evidence": ["SQU-4002903", "ZER-4000021", "SQU-4002483", "DWE-4001424", "ZER-4001287"]
  },
  {
    "endpoint": "/v1/listings",
    "category": "fraud",
    "documented": "posted_by_contact is the seller's verified contact number.",
    "actual": "Multiple non-genuine / lead-gen listings exist where identical phone numbers are reused across distinct properties with multiple fake agent/agency names or rental prices listed as sale prices.",
    "how_found": "Grouped listings by posted_by_contact and detected mismatched seller names and rental prices under Rs 1 Lakh.",
    "impact": "Users contacting sellers reach lead-gen agents or fake listing contacts.",
    "evidence": ["100-4000066", "100-4000158", "DWE-4000060", "MAG-4000075", "SQU-4000104"]
  },
  {
    "endpoint": "/v1/projects",
    "category": "consistency",
    "documented": "total_listings is recomputed whenever a listing is added or withdrawn, so it always agrees with GET /v1/listings?project_id=...",
    "actual": "total_listings reported in /v1/projects disagrees with actual listing count in /v1/listings for 336 out of 460 projects.",
    "how_found": "Compared project.total_listings against count of listings matching project_id.",
    "impact": "Project detail pages report inaccurate available inventory counts.",
    "evidence": ["P40001", "P40002", "P40003", "P40004", "P40005"]
  },
  {
    "endpoint": "/v1/analytics/summary",
    "category": "missing_endpoint",
    "documented": "GET /v1/analytics/summary returns pre-computed aggregates for your city.",
    "actual": "GET /v1/analytics/summary returns HTTP 404 Not Found.",
    "how_found": "Sent GET request to /v1/analytics/summary with valid auth headers.",
    "impact": "Insights / analytics dashboard cannot rely on server summary and must compute aggregates client-side.",
    "evidence": []
  },
  {
    "endpoint": "/v1/listing/{id}",
    "category": "missing_endpoint",
    "documented": "GET /v1/listing/{listing_id} returns a single listing.",
    "actual": "GET /v1/listing/{id} (singular listing) returns 404 Not Found. The working path is plural: GET /v1/listings/{id}.",
    "how_found": "Sent GET requests to /v1/listing/MAG-4001518 (404) vs /v1/listings/MAG-4001518 (200).",
    "impact": "Navigation to listing detail using documented singular URL path fails.",
    "evidence": []
  },
  {
    "endpoint": "/v1/listings/{id}/similar",
    "category": "missing_endpoint",
    "documented": "GET /v1/listings/{listing_id}/similar returns up to ten comparable listings.",
    "actual": "GET /v1/listings/{id}/similar returns HTTP 404 Not Found.",
    "how_found": "Sent GET request to /v1/listings/MAG-4001518/similar and received 404.",
    "impact": "Similar listings feature strips fail to load from server.",
    "evidence": []
  },
  {
    "endpoint": "/v1/favourites",
    "category": "missing_endpoint",
    "documented": "GET /v1/favourites, POST /v1/favourites, and DELETE /v1/favourites/{id} for saved listings.",
    "actual": "All /v1/favourites endpoints return HTTP 404 Not Found.",
    "how_found": "Sent GET, POST, DELETE requests to /v1/favourites and received 404.",
    "impact": "Saved listings must be managed and persisted on the client side.",
    "evidence": []
  },
  {
    "endpoint": "/auth/refresh",
    "category": "undocumented_endpoint",
    "documented": "Not mentioned in documentation. Doc states 'There is no refresh flow'.",
    "actual": "POST /auth/refresh exists and accepts refresh_token to issue a new access_token.",
    "how_found": "Discovered refresh_url in POST /auth/login response and tested POST /auth/refresh.",
    "impact": "Allows silent token renewal when 15-minute access token expires.",
    "evidence": []
  },
  {
    "endpoint": "/v1/listings",
    "category": "sorting",
    "documented": "Supports sort_by (price, carpet_area, posted_at, bedroom) and order (asc, desc).",
    "actual": "Sorting by price performs string/lexicographical sort or incorrect numerical order for negative prices, returning negative values first on desc order.",
    "how_found": "Passed sort_by=price&order=desc and inspected order of returned prices.",
    "impact": "Sorting listings by price fails to present correctly ordered results.",
    "evidence": []
  },
  {
    "endpoint": "/v1/listings",
    "category": "duplicates",
    "documented": "Each listing corresponds to exactly one physical property.",
    "actual": "Multiple listing records with distinct listing_ids exist for the exact same physical property (identical locality, apartment_name, floor, carpet_area, bhk, and facing_direction).",
    "how_found": "Grouped listings by physical property attributes.",
    "impact": "Duplicate property cards appear in search results.",
    "evidence": ["100-4000035", "MAG-4001518", "DWE-4001305"]
  }
]

submission_data = {
  "api_key": "IVY26-F90E52596CBD",
  "candidate": {
    "name": "Arushi Khare",
    "email": "arushi.khare@mnnit.ac.in",
    "repo_url": "https://github.com/arushikhare/ivy-homes-assignment",
    "demo_url": "https://ivy-homes-assignment.vercel.app"
  },
  "answers": answers,
  "findings": findings
}

with open(TARGET_FILE, "w") as f:
    json.dump(submission_data, f, indent=2)

print(f"Successfully generated {TARGET_FILE}!")
