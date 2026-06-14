from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    companies,
    customers,
    vehicles,
    drivers,
    trips,
    costs,
    invoices,
    profitability,
    upload,
    ai,
    seed,
)

app = FastAPI(
    title="LogiFlow API",
    description="Profitability analytics API for Belgian logistics SMEs",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


app.include_router(companies.router, prefix="/api/companies", tags=["companies"])
app.include_router(customers.router, prefix="/api/customers", tags=["customers"])
app.include_router(vehicles.router, prefix="/api/vehicles", tags=["vehicles"])
app.include_router(drivers.router, prefix="/api/drivers", tags=["drivers"])
app.include_router(trips.router, prefix="/api/trips", tags=["trips"])
app.include_router(costs.router, prefix="/api/costs", tags=["costs"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["invoices"])
app.include_router(profitability.router, prefix="/api/profitability", tags=["profitability"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])
app.include_router(seed.router, prefix="/api/seed", tags=["seed"])
