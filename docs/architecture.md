# LogiFlow — Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────┐
│                      User Browser                        │
└───────────────────────┬─────────────────────────────────┘
                        │ HTTPS
┌───────────────────────▼─────────────────────────────────┐
│              Next.js 14 (App Router)                     │
│         frontend/ — Port 3000                            │
│  - Google OAuth via NextAuth.js                          │
│  - Dashboard, Upload, AI Chat pages                      │
│  - Recharts for visualization                            │
└───────────────────────┬─────────────────────────────────┘
                        │ REST / JSON
┌───────────────────────▼─────────────────────────────────┐
│               FastAPI (Python 3.11)                      │
│         backend/ — Port 8000                             │
│  - JWT verification (Google tokens)                      │
│  - Business logic & profitability engine                 │
│  - CSV parsing & validation                              │
│  - OpenAI API calls for AI assistant                     │
└───────────┬───────────────────────┬─────────────────────┘
            │                       │
┌───────────▼──────────┐  ┌─────────▼───────────────────┐
│   PostgreSQL 16      │  │      OpenAI / Gemini API     │
│   Port 5432          │  │   (AI assistant endpoint)    │
│   Dev: local Docker  │  └─────────────────────────────┘
│   Prod: Cloud SQL    │
└──────────────────────┘
```

## Data Flow — CSV Upload

```
User uploads CSV
      │
      ▼
FastAPI /api/upload/trips
      │
      ▼
Column validation (required: origin, destination, revenue_eur, date)
      │
   ┌──┴──┐
   │Error│ → Return row-level errors to frontend
   └─────┘
      │ Valid
      ▼
Insert rows into trips table
      │
      ▼
Trigger profitability recalculation for company
      │
      ▼
Dashboard data refreshed on next fetch
```

## Data Flow — AI Assistant

```
User types: "Which route lost money last month?"
      │
      ▼
POST /api/ai/ask { question, company_id }
      │
      ▼
Load company summary data from DB
(revenue by route, cost by route, margins)
      │
      ▼
Build context prompt with data
      │
      ▼
OpenAI GPT-4o (or Gemini) API call
      │
      ▼
Return answer in user's language
```

## Authentication Flow

```
User clicks "Sign in with Google"
      │
      ▼
NextAuth.js → Google OAuth 2.0
      │
      ▼
Google returns ID token
      │
      ▼
NextAuth creates session, stores user in DB
      │
      ▼
Frontend sends JWT on every API call (Authorization: Bearer)
      │
      ▼
FastAPI verifies token signature with Google public keys
      │
      ▼
Request proceeds with company_id scope
```

## Technology Decisions

### Why FastAPI over Node.js
- Python ecosystem for data processing (pandas, numpy)
- Async by default with SQLAlchemy 2.0
- Auto-generated OpenAPI docs (useful for Google partner demos)
- Easy BigQuery client integration later

### Why PostgreSQL first, BigQuery later
- PostgreSQL handles the MVP scale (< 1M rows per company)
- BigQuery migration path: replace SQLAlchemy engine, keep the same API surface
- `route_performance` materialized view becomes the Looker Studio data source

### Why Next.js App Router
- Server Components reduce client bundle (important for mobile networks in rural Belgium)
- Built-in API routes can proxy to FastAPI during development
- Good Vercel deploy story as alternative to Cloud Run

## Deployment — Development

```bash
docker-compose up
```

Services:
- `postgres` on :5432
- `backend` on :8000 (hot-reload via uvicorn --reload)
- `frontend` on :3000 (hot-reload via Next.js dev server)

## Deployment — Production (Google Cloud)

```
Cloud Run (backend)
  ├── Reads DATABASE_URL → Cloud SQL (PostgreSQL)
  ├── Reads OPENAI_API_KEY from Secret Manager
  └── Scales to zero when idle

Cloud Run (frontend)
  ├── NEXTAUTH_URL = https://app.logiflow.be
  └── NEXT_PUBLIC_BACKEND_URL = https://api.logiflow.be

Cloud SQL (PostgreSQL 16)
  └── Private IP, europe-west1 (Belgium)

Cloud Storage
  └── CSV upload staging bucket

BigQuery (Phase 2)
  └── Synced from Cloud SQL via Datastream
  └── Powers Looker Studio reports
```

### Cloud Run Configuration

Backend `Dockerfile` uses `PORT` environment variable (Cloud Run convention):

```dockerfile
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
```

## Environment Variables

| Variable | Service | Description |
|---|---|---|
| `DATABASE_URL` | backend | PostgreSQL connection string |
| `GOOGLE_CLIENT_ID` | both | OAuth app client ID |
| `GOOGLE_CLIENT_SECRET` | both | OAuth app client secret |
| `NEXTAUTH_SECRET` | frontend | Random string for session encryption |
| `OPENAI_API_KEY` | backend | OpenAI API key |
| `STRIPE_SECRET_KEY` | backend | Stripe payments |
| `ENVIRONMENT` | backend | development / production |

## Future: BigQuery Migration

When moving from PostgreSQL to BigQuery:

1. In `backend/app/database.py`, swap SQLAlchemy async engine for `google-cloud-bigquery` client
2. Replace ORM queries in routers with BigQuery SQL
3. Set up Cloud Datastream to replicate PostgreSQL → BigQuery for historical data
4. Connect Looker Studio to `logiflow.route_performance` dataset
5. Apply for Google Cloud Partner Advantage (requires 3 customer deployments on GCP)
