import uuid
from fastapi import APIRouter

router = APIRouter()

STUB = [
    {"id": str(uuid.uuid4()), "plate": "1-ABC-234", "type": "truck", "brand": "Volvo", "model": "FH16", "fuel_type": "diesel", "capacity_kg": 24000, "active": True},
    {"id": str(uuid.uuid4()), "plate": "2-DEF-567", "type": "van", "brand": "Mercedes", "model": "Sprinter", "fuel_type": "diesel", "capacity_kg": 3500, "active": True},
    {"id": str(uuid.uuid4()), "plate": "3-GHI-890", "type": "truck", "brand": "DAF", "model": "XF", "fuel_type": "diesel", "capacity_kg": 20000, "active": False},
]


@router.get("/")
async def list_vehicles(company_id: str | None = None):
    return STUB


@router.get("/{vehicle_id}")
async def get_vehicle(vehicle_id: uuid.UUID):
    return STUB[0]


@router.post("/")
async def create_vehicle(data: dict):
    return {**data, "id": str(uuid.uuid4())}


@router.put("/{vehicle_id}")
async def update_vehicle(vehicle_id: uuid.UUID, data: dict):
    return {**data, "id": str(vehicle_id)}


@router.delete("/{vehicle_id}")
async def delete_vehicle(vehicle_id: uuid.UUID):
    return {"deleted": True}
