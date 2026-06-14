# LogiFlow — AI Operations Dashboard for Belgian Logistics

LogiFlow is a profitability dashboard and AI assistant for Belgian SME transport and logistics companies. Upload your Excel/CSV data and instantly see which routes, clients, drivers, and vehicles are profitable.

## The Problem

Small transport companies operate blind. They do not know:
- Which routes generate profit vs. loss
- Which clients are actually worth the effort
- Which vehicles cost too much to run
- Where fuel and toll costs are eating margin

## The Product

A web dashboard that connects your dispatch data, fuel records, and invoices — then shows you margin, delays, vehicle utilization, and forecasted workload. Includes an AI assistant you can ask in French, Dutch, or English.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 14 (App Router), TypeScript, Tailwind CSS |
| Backend | FastAPI (Python) |
| Database | PostgreSQL (dev), BigQuery (prod) |
| Auth | Google OAuth 2.0 |
| AI | OpenAI GPT-4o → Gemini/Vertex AI |
| Deployment | Docker Compose (dev), Google Cloud Run (prod) |
| Payments | Stripe |

## Getting Started

```bash
cp .env.example .env
# Fill in your secrets in .env
docker-compose up
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API docs: http://localhost:8000/docs

## Project Structure

```
frontend/     Next.js dashboard app
backend/      FastAPI REST API + AI endpoint
database/     PostgreSQL schema
docs/         Product spec, architecture, task backlog
```

## Documentation

- [Product Spec](docs/product.md)
- [Architecture](docs/architecture.md)
- [Build Tasks](docs/tasks.md)

## Target Market

Belgian logistics and transport SMEs (5–50 vehicles). Initial pilots in Brussels, Antwerp, Ghent, and Liège.

## Roadmap to Google

1. MVP SaaS with 2 pilot customers
2. Google Cloud Run deployment
3. BigQuery analytics layer
4. Google for Startups Cloud Program
5. Google Cloud Marketplace listing
