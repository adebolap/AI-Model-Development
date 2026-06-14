import uuid
from fastapi import APIRouter

router = APIRouter()

STUB = [
    {"id": str(uuid.uuid4()), "name": "Jean-Pierre Dumont", "license_class": "CE", "active": True, "trips_this_month": 18},
    {"id": str(uuid.uuid4()), "name": "Mohamed El Ouafi", "license_class": "CE", "active": True, "trips_this_month": 22},
    {"id": str(uuid.uuid4()), "name": "Lieve Vandenberghe", "license_class": "C", "active": True, "trips_this_month": 14},
]


@router.get("/")
async def list_drivers(company_id: str | None = None):
    return STUB


@router.get("/{driver_id}")
async def get_driver(driver_id: uuid.UUID):
    return STUB[0]


@router.post("/")
async def create_driver(data: dict):
    return {**data, "id": str(uuid.uuid4())}


@router.put("/{driver_id}")
async def update_driver(driver_id: uuid.UUID, data: dict):
    return {**data, "id": str(driver_id)}


@router.delete("/{driver_id}")
async def delete_driver(driver_id: uuid.UUID):
    return {"deleted": True}
