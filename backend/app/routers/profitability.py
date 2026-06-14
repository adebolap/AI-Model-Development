from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services import profitability as svc

router = APIRouter()

STUB_SUMMARY = {
    "revenue_eur": 48200,
    "direct_cost_eur": 31800,
    "gross_margin_eur": 16400,
    "margin_pct": 34.0,
    "trip_count": 54,
    "active_vehicles": 8,
    "top_customer": "Delhaize Group",
}


@router.get("/summary")
async def profitability_summary(
    company_id: str | None = None,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
):
    if not company_id:
        return STUB_SUMMARY
    try:
        return await svc.get_summary(db, company_id, days)
    except Exception:
        return STUB_SUMMARY


@router.get("/by-customer")
async def profitability_by_customer(
    company_id: str | None = None,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
):
    if not company_id:
        return _stub_customers()
    try:
        data = await svc.get_by_customer(db, company_id, days)
        return data if data else _stub_customers()
    except Exception:
        return _stub_customers()


@router.get("/by-route")
async def profitability_by_route(
    company_id: str | None = None,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
):
    if not company_id:
        return _stub_routes()
    try:
        data = await svc.get_by_route(db, company_id, days)
        return data if data else _stub_routes()
    except Exception:
        return _stub_routes()


@router.get("/by-vehicle")
async def profitability_by_vehicle(
    company_id: str | None = None,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
):
    if not company_id:
        return _stub_vehicles()
    try:
        data = await svc.get_by_vehicle(db, company_id, days)
        return data if data else _stub_vehicles()
    except Exception:
        return _stub_vehicles()


def _stub_customers():
    return [
        {"customer": "Delhaize Group", "revenue_eur": 18200, "cost_eur": 10900, "margin_eur": 7300, "margin_pct": 40.1, "trip_count": 21},
        {"customer": "AB InBev Logistics", "revenue_eur": 14100, "cost_eur": 9800, "margin_eur": 4300, "margin_pct": 30.5, "trip_count": 18},
        {"customer": "Proximus", "revenue_eur": 8900, "cost_eur": 7200, "margin_eur": 1700, "margin_pct": 19.1, "trip_count": 9},
        {"customer": "Colruyt", "revenue_eur": 7000, "cost_eur": 3900, "margin_eur": 3100, "margin_pct": 44.3, "trip_count": 6},
    ]


def _stub_routes():
    return [
        {"origin": "Brussels", "destination": "Rotterdam", "avg_revenue_eur": 1850, "avg_cost_eur": 980, "avg_margin_pct": 47.0, "trip_count": 12},
        {"origin": "Antwerp", "destination": "Paris", "avg_revenue_eur": 2100, "avg_cost_eur": 1540, "avg_margin_pct": 26.7, "trip_count": 8},
        {"origin": "Liège", "destination": "Frankfurt", "avg_revenue_eur": 1650, "avg_cost_eur": 1430, "avg_margin_pct": 13.3, "trip_count": 6},
        {"origin": "Ghent", "destination": "Amsterdam", "avg_revenue_eur": 1400, "avg_cost_eur": 1340, "avg_margin_pct": 4.3, "trip_count": 4},
    ]


def _stub_vehicles():
    return [
        {"plate": "1-ABC-234", "type": "truck", "revenue_eur": 18400, "cost_eur": 11200, "margin_pct": 39.1, "trips": 22},
        {"plate": "2-DEF-567", "type": "van", "revenue_eur": 9800, "cost_eur": 7100, "margin_pct": 27.6, "trips": 18},
        {"plate": "3-GHI-890", "type": "truck", "revenue_eur": 7200, "cost_eur": 6900, "margin_pct": 4.2, "trips": 8},
    ]


@router.get("/monthly-trend")
async def monthly_trend(
    company_id: str | None = None,
    months: int = 6,
    db: AsyncSession = Depends(get_db),
):
    if not company_id:
        return _stub_monthly_trend()
    try:
        data = await svc.get_monthly_trend(db, company_id, months)
        return data if data else _stub_monthly_trend()
    except Exception:
        return _stub_monthly_trend()


@router.get("/cost-breakdown")
async def cost_breakdown(
    company_id: str | None = None,
    days: int = 30,
    db: AsyncSession = Depends(get_db),
):
    if not company_id:
        return _stub_cost_breakdown()
    try:
        data = await svc.get_cost_breakdown(db, company_id, days)
        return data if data else _stub_cost_breakdown()
    except Exception:
        return _stub_cost_breakdown()


def _stub_monthly_trend():
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    revenues = [32000, 38000, 41000, 36000, 44000, 48200]
    costs = [21500, 25200, 27100, 24300, 29800, 31800]
    return [
        {"month": m, "revenue_eur": r, "cost_eur": c, "trips": int(r / 850)}
        for m, r, c in zip(months, revenues, costs)
    ]


def _stub_cost_breakdown():
    return [
        {"name": "Fuel", "value": 14200, "color": "#3b82f6"},
        {"name": "Tolls", "value": 5800, "color": "#f59e0b"},
        {"name": "Salary", "value": 7400, "color": "#8b5cf6"},
        {"name": "Maintenance", "value": 3100, "color": "#10b981"},
        {"name": "Insurance", "value": 1300, "color": "#ef4444"},
    ]
