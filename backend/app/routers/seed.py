from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.seed import seed_demo

router = APIRouter()


@router.post("/")
async def seed(db: AsyncSession = Depends(get_db)):
    """Populate the DB with demo data (Transport Dupont SPRL, 90 days of trips)."""
    return await seed_demo(db)
