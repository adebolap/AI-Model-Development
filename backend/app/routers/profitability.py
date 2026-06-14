from fastapi import APIRouter

router = APIRouter()


@router.get("/summary")
async def profitability_summary(company_id: str | None = None, period: str = "month"):
    return {
        "period": period,
        "revenue_eur": 48200,
        "direct_cost_eur": 31800,
        "gross_margin_eur": 16400,
        "margin_pct": 34.0,
        "trip_count": 54,
        "active_vehicles": 8,
        "top_customer": "Delhaize Group",
        "vs_previous_period": {
            "revenue_pct": 12.4,
            "margin_pct": 2.1,
        },
    }


@router.get("/by-customer")
async def profitability_by_customer(company_id: str | None = None, period: str = "month"):
    return [
        {"customer": "Delhaize Group", "revenue_eur": 18200, "cost_eur": 10900, "margin_eur": 7300, "margin_pct": 40.1, "trip_count": 21},
        {"customer": "AB InBev Logistics", "revenue_eur": 14100, "cost_eur": 9800, "margin_eur": 4300, "margin_pct": 30.5, "trip_count": 18},
        {"customer": "Proximus", "revenue_eur": 8900, "cost_eur": 7200, "margin_eur": 1700, "margin_pct": 19.1, "trip_count": 9},
        {"customer": "Colruyt", "revenue_eur": 7000, "cost_eur": 3900, "margin_eur": 3100, "margin_pct": 44.3, "trip_count": 6},
    ]


@router.get("/by-route")
async def profitability_by_route(company_id: str | None = None, period: str = "month"):
    return [
        {"origin": "Brussels", "destination": "Rotterdam", "avg_revenue_eur": 1850, "avg_cost_eur": 980, "avg_margin_pct": 47.0, "trip_count": 12},
        {"origin": "Antwerp", "destination": "Paris", "avg_revenue_eur": 2100, "avg_cost_eur": 1540, "avg_margin_pct": 26.7, "trip_count": 8},
        {"origin": "Liège", "destination": "Frankfurt", "avg_revenue_eur": 1650, "avg_cost_eur": 1430, "avg_margin_pct": 13.3, "trip_count": 6},
        {"origin": "Ghent", "destination": "Amsterdam", "avg_revenue_eur": 1400, "avg_cost_eur": 1340, "avg_margin_pct": 4.3, "trip_count": 4},
    ]


@router.get("/by-vehicle")
async def profitability_by_vehicle(company_id: str | None = None, period: str = "month"):
    return [
        {"plate": "1-ABC-234", "type": "truck", "revenue_eur": 18400, "cost_eur": 11200, "margin_pct": 39.1, "trips": 22, "utilization_pct": 88},
        {"plate": "2-DEF-567", "type": "van", "revenue_eur": 9800, "cost_eur": 7100, "margin_pct": 27.6, "trips": 18, "utilization_pct": 72},
        {"plate": "3-GHI-890", "type": "truck", "revenue_eur": 7200, "cost_eur": 6900, "margin_pct": 4.2, "trips": 8, "utilization_pct": 32},
    ]
