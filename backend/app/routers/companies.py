import uuid
from fastapi import APIRouter

router = APIRouter()

STUB = [
    {"id": str(uuid.uuid4()), "name": "Transport Dupont SPRL", "vat_number": "BE0123456789", "country": "BE", "city": "Liège", "plan_tier": "starter"},
    {"id": str(uuid.uuid4()), "name": "Vlaamse Logistiek NV", "vat_number": "BE0987654321", "country": "BE", "city": "Ghent", "plan_tier": "growth"},
]


@router.get("/")
async def list_companies():
    return STUB


@router.get("/{company_id}")
async def get_company(company_id: uuid.UUID):
    return STUB[0]


@router.post("/")
async def create_company(data: dict):
    return {**data, "id": str(uuid.uuid4())}


@router.put("/{company_id}")
async def update_company(company_id: uuid.UUID, data: dict):
    return {**data, "id": str(company_id)}


@router.delete("/{company_id}")
async def delete_company(company_id: uuid.UUID):
    return {"deleted": True}
