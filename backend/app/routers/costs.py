import uuid
from fastapi import APIRouter

router = APIRouter()

STUB_FUEL = [
    {"id": str(uuid.uuid4()), "date": "2026-06-01", "liters": 120, "cost_eur": 198, "station": "Q8 Antwerp"},
    {"id": str(uuid.uuid4()), "date": "2026-06-03", "liters": 95, "cost_eur": 157, "station": "Total Liège"},
]

STUB_OPERATING = [
    {"id": str(uuid.uuid4()), "category": "toll", "description": "Viapass June", "amount_eur": 340, "date": "2026-06-01"},
    {"id": str(uuid.uuid4()), "category": "maintenance", "description": "Oil change 1-ABC-234", "amount_eur": 220, "date": "2026-06-05"},
    {"id": str(uuid.uuid4()), "category": "salary", "description": "Driver hours June W1", "amount_eur": 1800, "date": "2026-06-07"},
]


@router.get("/fuel")
async def list_fuel_costs(company_id: str | None = None):
    return STUB_FUEL


@router.post("/fuel")
async def create_fuel_cost(data: dict):
    return {**data, "id": str(uuid.uuid4())}


@router.get("/operating")
async def list_operating_costs(company_id: str | None = None, category: str | None = None):
    if category:
        return [c for c in STUB_OPERATING if c["category"] == category]
    return STUB_OPERATING


@router.post("/operating")
async def create_operating_cost(data: dict):
    return {**data, "id": str(uuid.uuid4())}
