from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta


async def get_summary(db: AsyncSession, company_id: str, days: int = 30) -> dict:
    since = date.today() - timedelta(days=days)

    result = await db.execute(
        text("""
            SELECT
                COALESCE(SUM(t.revenue_eur), 0)                                   AS revenue_eur,
                COALESCE(SUM(COALESCE(fc.fuel_total, 0)), 0)
                  + COALESCE(SUM(COALESCE(oc.op_total, 0)), 0)                    AS direct_cost_eur,
                COUNT(t.id)                                                        AS trip_count
            FROM trips t
            LEFT JOIN (
                SELECT trip_id, SUM(cost_eur) AS fuel_total
                FROM fuel_costs WHERE trip_id IS NOT NULL
                GROUP BY trip_id
            ) fc ON fc.trip_id = t.id
            LEFT JOIN (
                SELECT trip_id, SUM(amount_eur) AS op_total
                FROM operating_costs WHERE trip_id IS NOT NULL
                GROUP BY trip_id
            ) oc ON oc.trip_id = t.id
            WHERE t.company_id = :company_id
              AND t.deleted_at IS NULL
              AND t.status = 'completed'
              AND DATE(t.departure_at) >= :since
        """),
        {"company_id": company_id, "since": since},
    )
    row = result.mappings().one_or_none()
    if not row:
        return _empty_summary()

    revenue = float(row["revenue_eur"] or 0)
    cost = float(row["direct_cost_eur"] or 0)
    margin = revenue - cost
    margin_pct = round((margin / revenue * 100), 1) if revenue else 0

    vehicle_count = await db.scalar(
        text("SELECT COUNT(*) FROM vehicles WHERE company_id = :cid AND active = true AND deleted_at IS NULL"),
        {"cid": company_id},
    )

    top_customer = await db.execute(
        text("""
            SELECT c.name, SUM(t.revenue_eur) AS rev
            FROM trips t JOIN customers c ON c.id = t.customer_id
            WHERE t.company_id = :cid AND t.deleted_at IS NULL AND DATE(t.departure_at) >= :since
            GROUP BY c.name ORDER BY rev DESC LIMIT 1
        """),
        {"cid": company_id, "since": since},
    )
    top = top_customer.mappings().one_or_none()

    return {
        "revenue_eur": round(revenue, 2),
        "direct_cost_eur": round(cost, 2),
        "gross_margin_eur": round(margin, 2),
        "margin_pct": margin_pct,
        "trip_count": int(row["trip_count"] or 0),
        "active_vehicles": int(vehicle_count or 0),
        "top_customer": top["name"] if top else None,
    }


async def get_by_customer(db: AsyncSession, company_id: str, days: int = 30) -> list:
    since = date.today() - timedelta(days=days)
    result = await db.execute(
        text("""
            SELECT
                c.name                                                              AS customer,
                COALESCE(SUM(t.revenue_eur), 0)                                    AS revenue_eur,
                COALESCE(SUM(COALESCE(fc.fuel_total, 0) + COALESCE(oc.op_total, 0)), 0) AS cost_eur,
                COUNT(t.id)                                                         AS trip_count
            FROM trips t
            JOIN customers c ON c.id = t.customer_id
            LEFT JOIN (
                SELECT trip_id, SUM(cost_eur) AS fuel_total
                FROM fuel_costs WHERE trip_id IS NOT NULL GROUP BY trip_id
            ) fc ON fc.trip_id = t.id
            LEFT JOIN (
                SELECT trip_id, SUM(amount_eur) AS op_total
                FROM operating_costs WHERE trip_id IS NOT NULL GROUP BY trip_id
            ) oc ON oc.trip_id = t.id
            WHERE t.company_id = :cid AND t.deleted_at IS NULL AND DATE(t.departure_at) >= :since
            GROUP BY c.name
            ORDER BY revenue_eur DESC
        """),
        {"cid": company_id, "since": since},
    )
    rows = result.mappings().all()
    out = []
    for r in rows:
        rev = float(r["revenue_eur"] or 0)
        cost = float(r["cost_eur"] or 0)
        margin = rev - cost
        out.append({
            "customer": r["customer"],
            "revenue_eur": round(rev, 2),
            "cost_eur": round(cost, 2),
            "margin_eur": round(margin, 2),
            "margin_pct": round(margin / rev * 100, 1) if rev else 0,
            "trip_count": int(r["trip_count"] or 0),
        })
    return out


async def get_by_route(db: AsyncSession, company_id: str, days: int = 30) -> list:
    since = date.today() - timedelta(days=days)
    result = await db.execute(
        text("""
            SELECT
                t.origin,
                t.destination,
                ROUND(AVG(t.revenue_eur)::numeric, 2)                              AS avg_revenue_eur,
                ROUND(AVG(COALESCE(fc.fuel_total, 0) + COALESCE(oc.op_total, 0))::numeric, 2) AS avg_cost_eur,
                ROUND(AVG(t.distance_km)::numeric, 1)                              AS avg_distance_km,
                COUNT(t.id)                                                         AS trip_count
            FROM trips t
            LEFT JOIN (
                SELECT trip_id, SUM(cost_eur) AS fuel_total
                FROM fuel_costs WHERE trip_id IS NOT NULL GROUP BY trip_id
            ) fc ON fc.trip_id = t.id
            LEFT JOIN (
                SELECT trip_id, SUM(amount_eur) AS op_total
                FROM operating_costs WHERE trip_id IS NOT NULL GROUP BY trip_id
            ) oc ON oc.trip_id = t.id
            WHERE t.company_id = :cid AND t.deleted_at IS NULL AND DATE(t.departure_at) >= :since
            GROUP BY t.origin, t.destination
            ORDER BY avg_revenue_eur - avg_cost_eur ASC
        """),
        {"cid": company_id, "since": since},
    )
    rows = result.mappings().all()
    out = []
    for r in rows:
        rev = float(r["avg_revenue_eur"] or 0)
        cost = float(r["avg_cost_eur"] or 0)
        out.append({
            "origin": r["origin"],
            "destination": r["destination"],
            "avg_revenue_eur": rev,
            "avg_cost_eur": cost,
            "avg_margin_pct": round((rev - cost) / rev * 100, 1) if rev else 0,
            "avg_distance_km": float(r["avg_distance_km"] or 0),
            "trip_count": int(r["trip_count"] or 0),
        })
    return out


async def get_by_vehicle(db: AsyncSession, company_id: str, days: int = 30) -> list:
    since = date.today() - timedelta(days=days)
    result = await db.execute(
        text("""
            SELECT
                v.plate,
                v.type,
                COALESCE(SUM(t.revenue_eur), 0)                                    AS revenue_eur,
                COALESCE(SUM(COALESCE(fc.fuel_total, 0) + COALESCE(oc.op_total, 0)), 0) AS cost_eur,
                COUNT(t.id)                                                         AS trips
            FROM vehicles v
            LEFT JOIN trips t ON t.vehicle_id = v.id
                AND t.deleted_at IS NULL AND DATE(t.departure_at) >= :since
            LEFT JOIN (
                SELECT trip_id, SUM(cost_eur) AS fuel_total
                FROM fuel_costs WHERE trip_id IS NOT NULL GROUP BY trip_id
            ) fc ON fc.trip_id = t.id
            LEFT JOIN (
                SELECT trip_id, SUM(amount_eur) AS op_total
                FROM operating_costs WHERE trip_id IS NOT NULL GROUP BY trip_id
            ) oc ON oc.trip_id = t.id
            WHERE v.company_id = :cid AND v.deleted_at IS NULL
            GROUP BY v.plate, v.type
            ORDER BY revenue_eur DESC
        """),
        {"cid": company_id, "since": since},
    )
    rows = result.mappings().all()
    out = []
    for r in rows:
        rev = float(r["revenue_eur"] or 0)
        cost = float(r["cost_eur"] or 0)
        out.append({
            "plate": r["plate"],
            "type": r["type"],
            "revenue_eur": round(rev, 2),
            "cost_eur": round(cost, 2),
            "margin_pct": round((rev - cost) / rev * 100, 1) if rev else 0,
            "trips": int(r["trips"] or 0),
        })
    return out


async def get_monthly_trend(db: AsyncSession, company_id: str, months: int = 6) -> list:
    result = await db.execute(
        text("""
            SELECT
                TO_CHAR(DATE_TRUNC('month', departure_at), 'Mon') AS month_label,
                DATE_TRUNC('month', departure_at)                  AS month_date,
                ROUND(SUM(t.revenue_eur)::numeric, 0)              AS revenue_eur,
                ROUND(
                    SUM(COALESCE(fc.fuel_total, 0) + COALESCE(oc.op_total, 0))::numeric, 0
                )                                                  AS cost_eur,
                COUNT(t.id)                                        AS trips
            FROM trips t
            LEFT JOIN (
                SELECT trip_id, SUM(cost_eur) AS fuel_total
                FROM fuel_costs WHERE trip_id IS NOT NULL GROUP BY trip_id
            ) fc ON fc.trip_id = t.id
            LEFT JOIN (
                SELECT trip_id, SUM(amount_eur) AS op_total
                FROM operating_costs WHERE trip_id IS NOT NULL GROUP BY trip_id
            ) oc ON oc.trip_id = t.id
            WHERE t.company_id = :cid
              AND t.deleted_at IS NULL
              AND t.status = 'completed'
              AND departure_at >= DATE_TRUNC('month', NOW()) - INTERVAL '1 month' * :months
            GROUP BY month_date, month_label
            ORDER BY month_date ASC
        """),
        {"cid": company_id, "months": months},
    )
    rows = result.mappings().all()
    return [
        {
            "month": r["month_label"],
            "revenue_eur": float(r["revenue_eur"] or 0),
            "cost_eur": float(r["cost_eur"] or 0),
            "trips": int(r["trips"] or 0),
        }
        for r in rows
    ]


async def get_cost_breakdown(db: AsyncSession, company_id: str, days: int = 30) -> list:
    since = date.today() - timedelta(days=days)
    fuel = await db.scalar(
        text("SELECT COALESCE(SUM(cost_eur), 0) FROM fuel_costs WHERE company_id = :cid AND date >= :since"),
        {"cid": company_id, "since": since},
    )
    op_result = await db.execute(
        text("""
            SELECT category, COALESCE(SUM(amount_eur), 0) AS total
            FROM operating_costs
            WHERE company_id = :cid AND date >= :since
            GROUP BY category
        """),
        {"cid": company_id, "since": since},
    )
    op_rows = op_result.mappings().all()
    category_map = {r["category"]: float(r["total"]) for r in op_rows}

    COLOR_MAP = {
        "fuel": "#3b82f6",
        "toll": "#f59e0b",
        "maintenance": "#10b981",
        "salary": "#8b5cf6",
        "insurance": "#ef4444",
        "admin": "#6b7280",
        "other": "#d1d5db",
    }

    out = [{"name": "Fuel", "value": round(float(fuel or 0), 2), "color": COLOR_MAP["fuel"]}]
    label_map = {
        "toll": "Tolls", "maintenance": "Maintenance", "salary": "Salary",
        "insurance": "Insurance", "admin": "Admin", "other": "Other",
    }
    for cat, label in label_map.items():
        if cat in category_map and category_map[cat] > 0:
            out.append({"name": label, "value": round(category_map[cat], 2), "color": COLOR_MAP[cat]})

    return out


def _empty_summary() -> dict:
    return {
        "revenue_eur": 0,
        "direct_cost_eur": 0,
        "gross_margin_eur": 0,
        "margin_pct": 0,
        "trip_count": 0,
        "active_vehicles": 0,
        "top_customer": None,
    }
