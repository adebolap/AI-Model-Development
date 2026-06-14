from fastapi import APIRouter, UploadFile, File, HTTPException
import io
import pandas as pd

router = APIRouter()

TRIPS_REQUIRED_COLUMNS = {"origin", "destination", "departure_date", "revenue_eur", "customer_name", "vehicle_plate"}
INVOICES_REQUIRED_COLUMNS = {"customer_name", "amount_eur", "issued_date", "status"}


def validate_columns(df: pd.DataFrame, required: set[str]) -> list[dict]:
    missing = required - set(df.columns.str.lower().str.strip())
    if missing:
        raise HTTPException(
            status_code=422,
            detail=f"Missing required columns: {', '.join(sorted(missing))}",
        )
    return []


@router.post("/trips")
async def upload_trips(file: UploadFile = File(...)):
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File must be under 10 MB")

    content = await file.read()
    try:
        if file.filename and file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(content))
        else:
            df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse file: {e}")

    df.columns = df.columns.str.lower().str.strip()
    validate_columns(df, TRIPS_REQUIRED_COLUMNS)

    errors = []
    for i, row in df.iterrows():
        if pd.isna(row.get("revenue_eur")) or not str(row.get("revenue_eur", "")).replace(".", "").isdigit():
            errors.append({"row": i + 2, "field": "revenue_eur", "error": "must be a number"})
        if pd.isna(row.get("origin")) or str(row.get("origin", "")).strip() == "":
            errors.append({"row": i + 2, "field": "origin", "error": "cannot be empty"})
        if pd.isna(row.get("destination")) or str(row.get("destination", "")).strip() == "":
            errors.append({"row": i + 2, "field": "destination", "error": "cannot be empty"})

    if errors:
        return {"success": False, "errors": errors, "rows_parsed": len(df)}

    return {"success": True, "rows_imported": len(df), "errors": []}


@router.post("/invoices")
async def upload_invoices(file: UploadFile = File(...)):
    if file.size and file.size > 10 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="File must be under 10 MB")

    content = await file.read()
    try:
        if file.filename and file.filename.endswith(".xlsx"):
            df = pd.read_excel(io.BytesIO(content))
        else:
            df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse file: {e}")

    df.columns = df.columns.str.lower().str.strip()
    validate_columns(df, INVOICES_REQUIRED_COLUMNS)

    errors = []
    for i, row in df.iterrows():
        if pd.isna(row.get("amount_eur")) or not str(row.get("amount_eur", "")).replace(".", "").isdigit():
            errors.append({"row": i + 2, "field": "amount_eur", "error": "must be a number"})

    if errors:
        return {"success": False, "errors": errors, "rows_parsed": len(df)}

    return {"success": True, "rows_imported": len(df), "errors": []}
