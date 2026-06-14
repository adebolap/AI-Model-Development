# LogiFlow — Build Task Backlog

Ordered list of 10 build tasks for the MVP. Each task maps to a single feature branch.

---

## Task 1 — Frontend Skeleton ✅ (Phase 1)

**Branch:** `feature/frontend-skeleton`

Build the Next.js app for the logistics profitability dashboard.

Deliverables:
- [x] Login page with Google OAuth button and product tagline
- [x] Dashboard layout with sidebar and top nav
- [x] Sidebar nav: Dashboard, Trips, Vehicles, Drivers, Upload, AI Assistant
- [x] Dashboard page with 6 KPI placeholder cards: Revenue, Costs, Margin, Margin %, Trips, Active Vehicles
- [x] Placeholder pages for Trips, Vehicles, Drivers, Upload

Acceptance criteria:
- `npm run dev` starts without errors
- All pages render without crashing
- TypeScript compiles with no errors

---

## Task 2 — Backend Skeleton ✅ (Phase 1)

**Branch:** `feature/backend-skeleton`

Build the FastAPI backend with all REST endpoints.

Deliverables:
- [x] FastAPI app with CORS and OpenAPI docs
- [x] Routers: companies, customers, vehicles, drivers, trips, costs, invoices, profitability
- [x] SQLAlchemy async models for all tables
- [x] Alembic migration: `001_initial_schema`
- [x] All endpoints return stub data in correct shape
- [x] Dockerfile for Cloud Run compatibility

Acceptance criteria:
- `uvicorn main:app` starts without errors
- `GET /api/profitability/summary` returns valid JSON
- `GET /docs` shows all routes in Swagger UI

---

## Task 3 — Database Schema ✅ (Phase 1)

**Branch:** `feature/database-schema`

Design and implement the PostgreSQL schema.

Tables: companies, customers, drivers, vehicles, trips, fuel_costs, operating_costs, invoices, route_performance (materialized view)

Acceptance criteria:
- `psql -f database/schema.sql` runs without errors on a clean PostgreSQL instance
- All foreign keys and indexes defined
- `alembic upgrade head` applies migration cleanly

---

## Task 4 — CSV Upload

**Branch:** `feature/csv-upload`

Add CSV upload for trips and invoices.

Deliverables:
- Upload page with drag-and-drop file input
- `POST /api/upload/trips` — parses CSV, validates required columns, inserts rows
- `POST /api/upload/invoices` — same pattern
- Required columns for trips: `origin`, `destination`, `departure_date`, `revenue_eur`, `customer_name`, `vehicle_plate`
- Required columns for invoices: `customer_name`, `amount_eur`, `issued_date`, `status`
- Row-level validation errors returned as JSON: `{ row: 3, field: "revenue_eur", error: "must be a number" }`
- Frontend shows validation errors per row

Acceptance criteria:
- Valid CSV inserts rows into DB
- Invalid CSV returns errors without inserting anything (transaction rollback)
- File > 10MB rejected with clear error

---

## Task 5 — Profitability Engine

**Branch:** `feature/profitability-engine`

Build the calculation engine for profitability analytics.

Deliverables:
- `GET /api/profitability/summary` — revenue, total_cost, gross_margin, margin_pct for date range
- `GET /api/profitability/by-customer` — per-customer breakdown
- `GET /api/profitability/by-route` — per origin→destination breakdown
- `GET /api/profitability/by-vehicle` — per vehicle breakdown
- Margin formula: `(revenue - direct_cost) / revenue * 100`
- Direct cost = fuel_costs + operating_costs allocated to trip

Acceptance criteria:
- Returns correct math for 10-row test dataset (verified manually)
- Handles companies with no data (returns zeros, not errors)
- Response time < 500ms for 10,000 trips

---

## Task 6 — Dashboard Charts

**Branch:** `feature/dashboard-charts`

Wire up real data to the dashboard with charts.

Deliverables:
- Monthly revenue trend line chart (Recharts)
- Top 5 customers bar chart by margin
- Low-margin routes table (sorted ascending by margin %)
- Vehicle utilization chart (trips per vehicle per month)
- Cost breakdown donut chart (fuel / tolls / maintenance / salary)

Acceptance criteria:
- Charts render with real data from API
- Empty states shown when no data uploaded
- Charts are responsive (mobile-friendly)

---

## Task 7 — AI Assistant

**Branch:** `feature/ai-assistant`

Add the AI Q&A endpoint and chat UI.

Deliverables:
- `POST /api/ai/ask` — takes `{ question: string, company_id: uuid }`, returns `{ answer: string }`
- Context building: load last 90 days of profitability summary before sending to LLM
- System prompt in English; detects question language and responds in same language (FR/NL/EN)
- Chat UI: message thread, input box, loading state
- AI Assistant page in sidebar nav

Acceptance criteria:
- "Which route lost money last month?" returns a factual answer based on DB data
- Response in French when question asked in French
- Graceful error when OpenAI API is unavailable

---

## Task 8 — Google OAuth Authentication

**Branch:** `feature/google-oauth`

Add full authentication with Google OAuth.

Deliverables:
- NextAuth.js with Google provider
- Protected routes: redirect to `/login` if not authenticated
- Backend JWT verification middleware
- User model: google_id, email, name, avatar_url
- Company association: user can belong to 1+ companies

Acceptance criteria:
- Sign in with Google works end-to-end
- API calls rejected with 401 if no valid token
- Session persists across browser refresh

---

## Task 9 — Dockerize

**Branch:** `feature/docker`

Containerize frontend and backend.

Deliverables:
- `backend/Dockerfile` — multi-stage, production-ready, uses `PORT` env var
- `frontend/Dockerfile` — multi-stage Next.js build
- `docker-compose.yml` — local dev with hot reload
- `.env.example` with all required variables

Acceptance criteria:
- `docker-compose up` starts all 3 services cleanly
- Frontend hot-reload works with volume mount
- Production build: `docker build -t logiflow-backend ./backend` succeeds

---

## Task 10 — Google Cloud Run Deployment

**Branch:** `feature/cloud-run`

Prepare and deploy to Google Cloud Run.

Deliverables:
- `cloudbuild.yaml` — Cloud Build CI/CD trigger
- `backend/cloud-run.yaml` — Cloud Run service manifest
- `frontend/cloud-run.yaml` — Cloud Run service manifest
- Secret Manager integration for API keys
- Cloud SQL connection via unix socket
- Health check endpoints: `GET /health` (backend), `GET /api/health` (frontend proxy)
- `docs/deployment.md` — step-by-step GCP setup guide

Acceptance criteria:
- `gcloud run deploy` succeeds
- App accessible at `https://app.logiflow.be` (or Cloud Run URL)
- All secrets loaded from Secret Manager (no env vars hardcoded in image)
