import uuid
from fastapi import APIRouter

router = APIRouter()

STUB = [
    {"id": str(uuid.uuid4()), "origin": "Brussels", "destination": "Rotterdam", "revenue_eur": 1850, "distance_km": 210, "status": "completed"},
    {"id": str(uuid.uuid4()), "origin": "Antwerp", "destination": "Paris", "revenue_eur": 2100, "distance_km": 340, "status": "completed"},
    {"id": str(uuid.uuid4()), "origin": "Liège", "destination": "Frankfurt", "revenue_eur": 1650, "distance_km": 280, "status": "in_progress"},
]


@router.get("/")
async def list_trips(company_id: str | None = None, status: str | None = None):
    return STUB


@router.get("/{trip_id}")
async def get_trip(trip_id: uuid.UUID):
    return STUB[0]


@router.post("/")
async def create_trip(data: dict):
    return {**data, "id": str(uuid.uuid4())}


@router.put("/{trip_id}")
async def update_trip(trip_id: uuid.UUID, data: dict):
    return {**data, "id": str(trip_id)}


@router.delete("/{trip_id}")
async def delete_trip(trip_id: uuid.UUID):
    return {"deleted": True}
