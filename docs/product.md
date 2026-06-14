# LogiFlow — Product Specification

## Problem Statement

Belgian SME transport and logistics companies (5–50 vehicles) operate without profitability visibility. They rely on spreadsheets, gut feel, and end-of-year accountant summaries to understand performance.

They cannot answer:
- Is route Brussels → Rotterdam profitable after fuel, tolls, and driver hours?
- Is customer Delhaize worth the 3 extra stops they demand?
- Which vehicle costs more to run than it earns?
- What will next month's workload look like?

This costs them 10–20% margin leakage per year on average.

---

## Target Personas

### 1. Fleet Manager (primary)
- Manages 5–30 trucks
- Drowning in WhatsApp messages, spreadsheets, and paper delivery notes
- Wants: know which driver/vehicle/route is profitable without building it in Excel
- Pain: no time to build reports, no budget for enterprise software

### 2. Owner-Operator (primary)
- 1–5 trucks, does everything themselves
- Invoices in Word, fuel receipts in a shoebox
- Wants: one place to see if they are making money
- Pain: accountant only tells them 6 months later

### 3. Finance / Operations Coordinator (secondary)
- Works at a mid-sized logistics company (20–100 vehicles)
- Already uses TMS software, but no profitability layer
- Wants: dashboard that pulls from their existing exports
- Pain: custom BI tools cost €20k+/year

---

## Core Features — Version 1.0

### 1. CSV / Excel Import
- Upload trips, invoices, fuel costs in CSV format
- Column mapping UI for non-standard exports
- Validation errors shown per row with clear messages
- Supported formats: CSV, XLSX

### 2. Profitability Dashboard
- KPI cards: Revenue, Direct Costs, Gross Margin, Margin %, Trips, Active Vehicles
- Monthly revenue trend chart
- Top 5 customers by revenue and margin
- Low-margin routes table (sorted by margin %)
- Vehicle utilization heatmap
- Cost breakdown: fuel / tolls / maintenance / salary

### 3. AI Assistant
- Natural language Q&A over company data
- Languages: French, Dutch, English
- Example questions:
  - "Which route lost money last month?"
  - "Quel client a la meilleure marge?"
  - "Welke chauffeur rijdt het meest overuren?"
- Powered by OpenAI GPT-4o (MVP), migrated to Gemini/Vertex AI for Google alignment

### 4. Authentication
- Google OAuth 2.0 sign-in
- Multi-company: one account can manage multiple company profiles
- Role-based: Admin, Manager, Viewer

---

## Pricing Model

| Tier | Price | Limits |
|---|---|---|
| Free | €0 | 1 company, 50 trips/month, no AI |
| Starter | €49/mo | 1 company, unlimited trips, AI assistant |
| Growth | €149/mo | 3 companies, API access, priority support |
| Enterprise | Custom | Unlimited, BigQuery sync, Looker reports |

Annual discount: 20%.

---

## Languages

- French (fr-BE) — primary for Wallonia, Brussels
- Dutch (nl-BE) — primary for Flanders
- English (en) — secondary for international operators

---

## Regulatory Notes (Belgium)

- VAT number format: BE0123456789
- Belgian truck toll (viapass) data can be imported as CSV
- GDPR compliance required: data stored in EU (Google Cloud Belgium region: europe-west1)
- Social dumping regulations: driver hours must be trackable

---

## Success Metrics (90-day pilot)

- 2 paying pilot customers by Day 75
- NPS > 40 from pilot users
- 3 case study data points (routes analyzed, margin found, time saved)
- Google Cloud Run deployment live
- Partner-ready demo environment
