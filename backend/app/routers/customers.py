import uuid
from fastapi import APIRouter

router = APIRouter()

STUB = [
    {"id": str(uuid.uuid4()), "name": "Delhaize Group", "city": "Brussels", "country": "BE", "revenue_eur": 48200},
    {"id": str(uuid.uuid4()), "name": "AB InBev Logistics", "city": "Leuven", "country": "BE", "revenue_eur": 32100},
    {"id": str(uuid.uuid4()), "name": "Proximus", "city": "Brussels", "country": "BE", "revenue_eur": 18900},
]


@router.get("/")
async def list_customers(company_id: str | None = None):
    return STUB


@router.get("/{customer_id}")
async def get_customer(customer_id: uuid.UUID):
    return STUB[0]


@router.post("/")
async def create_customer(data: dict):
    return {**data, "id": str(uuid.uuid4())}


@router.put("/{customer_id}")
async def update_customer(customer_id: uuid.UUID, data: dict):
    return {**data, "id": str(customer_id)}


@router.delete("/{customer_id}")
async def delete_customer(customer_id: uuid.UUID):
    return {"deleted": True}
