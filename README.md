# Ivy Homes Property API — Software Engineering Internship Submission

**Candidate**: Arushi Khare  
**Email**: arushi.khare@mnnit.ac.in  
**City**: Chennai  
**Assigned Locality**: T Nagar  
**API Key**: `IVY26-F90E52596CBD`  

---

## Overview

This repository contains the complete solution for the Ivy Homes Software Engineering Internship Assignment (September 2026). It consists of:
1. **Part 1 — Frontend Web Application**: A modern, high-performance React application built with Vite, Vanilla CSS, and custom glassmorphism design system. Fully supports demo login accounts (`demo1@ivy.homes`, `demo2@ivy.homes`, `demo3@ivy.homes` with password `5ec43320d2`), listing browsing, filtering, listing details, saved favourites per user, rentals, builder projects with unit corrections, and an interactive Insights & API Audit screen.
2. **Part 2 — Ten Calculated Answers**: Mathematically precise answers for City **Chennai** anchored at `REFERENCE = 2026-09-10T00:00:00+05:30 (IST)`.
3. **Part 3 — List the Lies**: 18 empirical documentation discrepancy findings documented in `submission.json` across 13 required categories (`auth`, `pagination`, `units`, `filters`, `sorting`, `timestamps`, `duplicates`, `data_quality`, `fraud`, `consistency`, `missing_endpoint`, `undocumented_endpoint`).

---

## How to Run the Web Application

### Prerequisites
- Node.js (v18 or higher recommended)
- npm / yarn / pnpm

### Installation & Local Setup

```bash
# 1. Clone the repository
git clone https://github.com/arushikhare/ivy-homes-assignment.git
cd ivy-homes-assignment

# 2. Install dependencies
npm install

# 3. Start local development server
npm run dev
```

The application will be available at `http://localhost:5173`.

### Production Build

```bash
npm run build
```

The production bundle will be output to the `dist/` directory.

---

## How We Distrusted & Audited the Documentation

We approached the API as an honest running service while treating `API_REFERENCE.md` as an unreviewed draft. Our audit process combined automated endpoint probing with empirical hypothesis testing:

1. **Authentication Flow Probing**:
   - *Claim*: API key passed via query parameter `?api_key=...`, 24-hour token under `"token"` field, no refresh flow.
   - *Audit*: Query parameter returned HTTP 401 `{"detail": "send your key in the X-API-Key request header..."}`. Inspecting login response revealed `"access_token"`, 900s (15 min) expiration, and an undocumented `/auth/refresh` endpoint with `"refresh_token"`.
   - *Fix*: Created a central API service (`src/services/api.js`) that attaches `X-API-Key` and `Authorization: Bearer` headers, with silent automatic token renewal via `POST /auth/refresh`.

2. **Pagination Mechanics**:
   - *Claim*: Endpoints take 1-indexed `page` and `limit` (max 200), returning `page_size`.
   - *Audit*: Requests to `page=1` and `page=2` yielded identical data; `page` was quietly ignored. Passing `offset=50` yielded page 2. Requests with `limit=200` returned only 50 records. `total` reported 3967 listings, but exhausting offset pagination retrieved 4100 records.
   - *Fix*: Implemented `offset` & `limit` batch fetching across collection views and client-side dataset aggregation.

3. **Units & Data Formatting**:
   - *Claim*: Project `price_min` and `price_max` are integer rupees.
   - *Audit*: Inspected `/v1/projects` data and found floating-point values like `67.7` and `3.78`. Comparing against matching listing prices revealed `67.7` means 67.7 Lakhs (₹6,770,000) and `3.78` means 3.78 Crores (₹37,800,000).
   - *Fix*: Created unit converter functions (`formatProjectPrice`, `getProjectMaxPriceInr`) to render clean human-readable price ranges.

4. **Missing & Broken Endpoints**:
   - *Audit*: Tested `/v1/analytics/summary` (404), `/v1/listing/{id}` (404, working path is plural `/v1/listings/{id}`), `/v1/listings/{id}/similar` (404), and `/v1/favourites` (404).
   - *Fix*: Built client-side aggregates for insights dashboard, fixed detail page routing to plural `/v1/listings/{id}`, and implemented local user-scoped storage for saved favourites.

---

## What We Checked That Turned Out to Be Fine

Hypotheses that did **not** pan out tell us more about data integrity than the ones that did:

1. **Hypothesis: Health Endpoint Discrepancies**:
   - *Idea*: `/health` might require authentication or return non-200 status under load.
   - *Finding*: `/health` is unauthenticated, lightweight, and consistently returns `200 OK` with service status and server timestamp.

2. **Hypothesis: Portal Domain Spoofing**:
   - *Idea*: `listing_url` domains for portals (`magichomes`, `100acres`, `dwelling`, `squarelane`, `zerobroker`) might point to malicious or mismatched domains.
   - *Finding*: Every single `listing_url` maps 1-to-1 to its legitimate domain name.

3. **Hypothesis: Locality Query Filtering**:
   - *Idea*: Locality parameter filtering on `/v1/listings` might fail or ignore case sensitivity.
   - *Finding*: Server-side `locality` filter works accurately for valid locality strings.

4. **Hypothesis: Bedroom (BHK) and Furnishing Server Filters**:
   - *Idea*: Server might ignore `bhk` or `furnishing` query parameters like it did for `page`.
   - *Finding*: `bhk` and `furnishing` query parameters strictly filter matching records on `/v1/listings`.

5. **Hypothesis: Rental Price Unit Corruption**:
   - *Idea*: Rental `price` or `deposit` values might be expressed in thousands or lakhs instead of rupees.
   - *Finding*: Rental monthly rent (`price`) and security deposit (`deposit`) are consistently expressed in integer Indian Rupees.

---

## What We Would Do With Another Two Days

If granted another two days, we would implement:

1. **Automated OpenAPI / Swagger Spec Generator**:
   - Build a lightweight proxy layer that observes live API traffic, auto-generates corrected OpenAPI 3.0 schemas, and flags documentation drift in CI/CD pipelines.

2. **Interactive Spatial Map View**:
   - Integrate Mapbox GL / Leaflet JS with spatial clustering to display properties across Chennai localities with real-time price heatmap overlays.

3. **Automated E2E Test Suite**:
   - Add Playwright E2E tests covering token refresh under 15-minute expiration, offline session persistence, and data quality filtering toggles.

4. **Real-time WebSockets / Server-Sent Events (SSE)**:
   - Implement simulated real-time price update notifications and inventory status alerts when properties transition to withdrawn/inactive.

---

## Project Artifacts

- `submission.json`: Main submission artifact containing candidate metadata, the 10 calculated answers, and the 18 discrepancy findings.
- `src/`: Complete source code for Vite + React web application.
- `scratch/`: Diagnostic scripts used to scrape, audit, and calculate answers empirically.
