import io
import uuid
from datetime import date

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db

router = APIRouter()

TRIPS_REQUIRED = {"origin", "destination", "departure_date", "revenue_eur", "customer_name", "vehicle_plate"}
INVOICES_REQUIRED = {"customer_name", "amount_eur", "issued_date", "status"}


def _parse_file(content: bytes, filename: str) -> pd.DataFrame:
    if filename.endswith(".xlsx"):
        df = pd.read_excel(io.BytesIO(content))
    else:
        df = pd.read_csv(io.BytesIO(content))
    df.columns = df.columns.str.lower().str.strip()
    return df


def _check_columns(df: pd.DataFrame, required: set[str]):
    missing = required - set(df.columns)
    if missing:
        raise HTTPException(status_code=422, detail=f"Missing columns: {', '.join(sorted(missing))}")


async def _get_or_create_customer(db: AsyncSession, company_id: str, name: str) -> str:
    row = await db.scalar(
        text("SELECT id FROM customers WHERE company_id = :cid AND name = :name LIMIT 1"),
        {"cid": company_id, "name": name},
    )
    if row:
        return str(row)
    cid = str(uuid.uuid4())
    await db.execute(
        text("INSERT INTO customers (id, company_id, name) VALUES (:id, :cid, :name)"),
        {"id": cid, "cid": company_id, "name": name},
    )
    return cid


async def _get_or_create_vehicle(db: AsyncSession, company_id: str, plate: str) -> str:
    row = await db.scalar(
        text("SELECT id FROM vehicles WHERE company_id = :cid AND plate = :plate LIMIT 1"),
        {"cid": company_id, "plate": plate},
    )
    if row:
        return str(row)
    vid = str(uuid.uuid4())
    await db.execute(
        text("INSERT INTO vehicles (id, company_id, plate, fuel_type) VALUES (:id, :cid, :plate, 'diesel')"),
        {"id": vid, "cid": company_id, "plate": plate},
    )
    return vid


def _to_float(val) -> float | None:
    try:
        return float(str(val).replace(",", ".").strip())
    except (ValueError, TypeError):
        return None


def _to_date(val) -> date | None:
    if pd.isna(val):
        return None
    try:
        return pd.to_datetime(val).date()
    except Exception:
        return None


@router.post("/trips")
async def upload_trips(
    file: UploadFile = File(...),
    company_id: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File must be under 10 MB")

    content = await file.read()
    try:
        df = _parse_file(content, file.filename or "")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse file: {e}")

    _check_columns(df, TRIPS_REQUIRED)

    errors = []
    for i, row in df.iterrows():
        row_num = int(i) + 2
        rev = _to_float(row.get("revenue_eur"))
        if rev is None:
            errors.append({"row": row_num, "field": "revenue_eur", "error": "must be a number"})
        if not str(row.get("origin", "")).strip():
            errors.append({"row": row_num, "field": "origin", "error": "cannot be empty"})
        if not str(row.get("destination", "")).strip():
            errors.append({"row": row_num, "field": "destination", "error": "cannot be empty"})
        if not str(row.get("customer_name", "")).strip():
            errors.append({"row": row_num, "field": "customer_name", "error": "cannot be empty"})

    if errors:
        return {"success": False, "errors": errors, "rows_parsed": len(df)}

    if not company_id:
        return {"success": True, "rows_imported": len(df), "errors": [], "note": "No company_id — rows validated but not saved"}

    imported = 0
    try:
        for _, row in df.iterrows():
            customer_id = await _get_or_create_customer(db, company_id, str(row["customer_name"]).strip())
            vehicle_id = await _get_or_create_vehicle(db, company_id, str(row["vehicle_plate"]).strip())
            dep_date = _to_date(row.get("departure_date"))
            distance = _to_float(row.get("distance_km"))
            revenue = _to_float(row.get("revenue_eur")) or 0

            await db.execute(
                text("""
                    INSERT INTO trips
                        (id, company_id, customer_id, vehicle_id, origin, destination,
                         departure_at, distance_km, revenue_eur, status)
                    VALUES
                        (:id, :cid, :custid, :vid, :orig, :dest,
                         :dep, :dist, :rev, 'completed')
                """),
                {
                    "id": str(uuid.uuid4()),
                    "cid": company_id,
                    "custid": customer_id,
                    "vid": vehicle_id,
                    "orig": str(row["origin"]).strip(),
                    "dest": str(row["destination"]).strip(),
                    "dep": dep_date,
                    "dist": distance,
                    "rev": revenue,
                },
            )
            imported += 1

        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {e}")

    return {"success": True, "rows_imported": imported, "errors": []}


@router.post("/invoices")
async def upload_invoices(
    file: UploadFile = File(...),
    company_id: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File must be under 10 MB")

    content = await file.read()
    try:
        df = _parse_file(content, file.filename or "")
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse file: {e}")

    _check_columns(df, INVOICES_REQUIRED)

    errors = []
    for i, row in df.iterrows():
        row_num = int(i) + 2
        if _to_float(row.get("amount_eur")) is None:
            errors.append({"row": row_num, "field": "amount_eur", "error": "must be a number"})
        if not str(row.get("customer_name", "")).strip():
            errors.append({"row": row_num, "field": "customer_name", "error": "cannot be empty"})

    if errors:
        return {"success": False, "errors": errors, "rows_parsed": len(df)}

    if not company_id:
        return {"success": True, "rows_imported": len(df), "errors": [], "note": "No company_id — rows validated but not saved"}

    imported = 0
    valid_statuses = {"draft", "sent", "paid", "overdue", "cancelled"}
    try:
        for _, row in df.iterrows():
            customer_id = await _get_or_create_customer(db, company_id, str(row["customer_name"]).strip())
            status = str(row.get("status", "draft")).strip().lower()
            if status not in valid_statuses:
                status = "draft"
            issued = _to_date(row.get("issued_date")) or date.today()
            amount = _to_float(row.get("amount_eur")) or 0

            await db.execute(
                text("""
                    INSERT INTO invoices
                        (id, company_id, customer_id, amount_eur, issued_at, status)
                    VALUES
                        (:id, :cid, :custid, :amt, :issued, :status)
                """),
                {
                    "id": str(uuid.uuid4()),
                    "cid": company_id,
                    "custid": customer_id,
                    "amt": amount,
                    "issued": issued,
                    "status": status,
                },
            )
            imported += 1

        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Import failed: {e}")

    return {"success": True, "rows_imported": imported, "errors": []}
