import uuid
from fastapi import APIRouter

router = APIRouter()

STUB = [
    {"id": str(uuid.uuid4()), "invoice_number": "INV-2026-001", "amount_eur": 1850, "status": "paid", "issued_at": "2026-06-01"},
    {"id": str(uuid.uuid4()), "invoice_number": "INV-2026-002", "amount_eur": 2100, "status": "sent", "issued_at": "2026-06-05"},
    {"id": str(uuid.uuid4()), "invoice_number": "INV-2026-003", "amount_eur": 950, "status": "overdue", "issued_at": "2026-05-10"},
]


@router.get("/")
async def list_invoices(company_id: str | None = None, status: str | None = None):
    if status:
        return [i for i in STUB if i["status"] == status]
    return STUB


@router.get("/{invoice_id}")
async def get_invoice(invoice_id: uuid.UUID):
    return STUB[0]


@router.post("/")
async def create_invoice(data: dict):
    return {**data, "id": str(uuid.uuid4())}


@router.put("/{invoice_id}")
async def update_invoice(invoice_id: uuid.UUID, data: dict):
    return {**data, "id": str(invoice_id)}


@router.delete("/{invoice_id}")
async def delete_invoice(invoice_id: uuid.UUID):
    return {"deleted": True}
