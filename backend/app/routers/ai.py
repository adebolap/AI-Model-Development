from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import settings
from app.database import get_db
from app.services.profitability import get_summary, get_by_customer, get_by_route

router = APIRouter()


class AskRequest(BaseModel):
    question: str
    company_id: str | None = None


STUB_CONTEXT = """
Company: Transport Dupont SPRL (demo)
Period: Last 30 days
Revenue: €48,200 | Costs: €31,800 | Margin: 34%
Top route: Brussels → Rotterdam (margin 47%)
Worst route: Ghent → Amsterdam (margin 4.3%)
Top customer: Delhaize Group (margin 40%) | Lowest: Proximus (margin 19%)
Active vehicles: 8 | Trips: 54
"""


async def _build_context(db: AsyncSession, company_id: str) -> str:
    try:
        s = await get_summary(db, company_id)
        routes = await get_by_route(db, company_id)
        customers = await get_by_customer(db, company_id)

        best_route = max(routes, key=lambda r: r["avg_margin_pct"], default=None) if routes else None
        worst_route = min(routes, key=lambda r: r["avg_margin_pct"], default=None) if routes else None
        top_cust = customers[0] if customers else None
        low_cust = customers[-1] if customers else None

        lines = [
            f"Revenue (30d): €{s['revenue_eur']:,.0f}",
            f"Costs (30d): €{s['direct_cost_eur']:,.0f}",
            f"Margin: €{s['gross_margin_eur']:,.0f} ({s['margin_pct']}%)",
            f"Trips: {s['trip_count']} | Active vehicles: {s['active_vehicles']}",
        ]
        if best_route:
            lines.append(f"Best route: {best_route['origin']} → {best_route['destination']} (margin {best_route['avg_margin_pct']}%)")
        if worst_route and worst_route != best_route:
            lines.append(f"Worst route: {worst_route['origin']} → {worst_route['destination']} (margin {worst_route['avg_margin_pct']}%)")
        if top_cust:
            lines.append(f"Top customer: {top_cust['customer']} (margin {top_cust['margin_pct']}%)")
        if low_cust and low_cust != top_cust:
            lines.append(f"Lowest margin customer: {low_cust['customer']} (margin {low_cust['margin_pct']}%)")
        if routes:
            lines.append("\nAll routes (sorted by margin):")
            for r in sorted(routes, key=lambda x: x["avg_margin_pct"]):
                lines.append(f"  {r['origin']} → {r['destination']}: avg revenue €{r['avg_revenue_eur']}, margin {r['avg_margin_pct']}%, {r['trip_count']} trips")

        return "\n".join(lines)
    except Exception:
        return STUB_CONTEXT


@router.post("/ask")
async def ask_ai(body: AskRequest, db: AsyncSession = Depends(get_db)):
    if not body.question.strip():
        raise HTTPException(status_code=422, detail="Question cannot be empty")

    context = await _build_context(db, body.company_id) if body.company_id else STUB_CONTEXT

    if not settings.openai_api_key:
        return {
            "answer": (
                f"AI assistant needs OPENAI_API_KEY configured. "
                f"Based on your data:\n\n{context}\n\n"
                f"Your question: {body.question}"
            ),
            "model": "stub",
        }

    try:
        from openai import AsyncOpenAI
        client = AsyncOpenAI(api_key=settings.openai_api_key)

        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a logistics profitability analyst for a Belgian transport company. "
                        "Answer questions using only the data provided. Be concise and actionable. "
                        "Respond in the same language as the question (French, Dutch, or English). "
                        "If the data doesn't contain the answer, say so clearly.\n\n"
                        f"Company data:\n{context}"
                    ),
                },
                {"role": "user", "content": body.question},
            ],
            max_tokens=500,
            temperature=0.2,
        )
        return {"answer": response.choices[0].message.content, "model": "gpt-4o"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"AI service unavailable: {e}")
