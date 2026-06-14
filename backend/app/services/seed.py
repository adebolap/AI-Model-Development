"""
Creates a demo company with realistic Belgian logistics data.
Run once via POST /api/seed to populate the DB for development/demo.
"""

import uuid
from datetime import date, timedelta, datetime
import random
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


ROUTES = [
    ("Brussels", "Rotterdam", 210, 1850),
    ("Antwerp", "Paris", 340, 2100),
    ("Liège", "Frankfurt", 280, 1650),
    ("Ghent", "Amsterdam", 190, 1400),
    ("Brussels", "Luxembourg", 180, 1300),
    ("Antwerp", "Cologne", 220, 1550),
    ("Brussels", "London", 380, 2800),
    ("Ghent", "Lille", 70, 750),
]

CUSTOMERS = [
    ("Delhaize Group", "BE0447839156", "Brussels"),
    ("AB InBev Logistics", "BE0409966764", "Leuven"),
    ("Proximus", "BE0202239951", "Brussels"),
    ("Colruyt Group", "BE0400378485", "Halle"),
    ("Katoen Natie", "BE0400555870", "Antwerp"),
]

VEHICLES = [
    ("1-ABC-234", "truck", "Volvo", "FH16", "diesel", 24000),
    ("2-DEF-567", "van", "Mercedes", "Sprinter", "diesel", 3500),
    ("3-GHI-890", "truck", "DAF", "XF", "diesel", 20000),
    ("4-JKL-123", "truck", "MAN", "TGX", "diesel", 22000),
    ("5-MNO-456", "van", "Ford", "Transit", "diesel", 2800),
]

DRIVERS = [
    ("Jean-Pierre Dumont", "CE"),
    ("Mohamed El Ouafi", "CE"),
    ("Lieve Vandenberghe", "C"),
    ("Fatima Oualid", "CE"),
]


async def seed_demo(db: AsyncSession) -> dict:
    existing = await db.scalar(text("SELECT id FROM companies WHERE vat_number = 'BE0123456789' LIMIT 1"))
    if existing:
        return {"status": "already_seeded", "company_id": str(existing)}

    company_id = str(uuid.uuid4())
    await db.execute(
        text("""INSERT INTO companies (id, name, vat_number, country, city, plan_tier)
                VALUES (:id, :name, :vat, 'BE', 'Liège', 'starter')"""),
        {"id": company_id, "name": "Transport Dupont SPRL", "vat": "BE0123456789"},
    )

    customer_ids = []
    for name, vat, city in CUSTOMERS:
        cid = str(uuid.uuid4())
        customer_ids.append(cid)
        await db.execute(
            text("""INSERT INTO customers (id, company_id, name, vat_number, city, country)
                    VALUES (:id, :cid, :name, :vat, :city, 'BE')"""),
            {"id": cid, "cid": company_id, "name": name, "vat": vat, "city": city},
        )

    vehicle_ids = []
    for plate, vtype, brand, model, fuel, capacity in VEHICLES:
        vid = str(uuid.uuid4())
        vehicle_ids.append(vid)
        await db.execute(
            text("""INSERT INTO vehicles (id, company_id, plate, type, brand, model, fuel_type, capacity_kg)
                    VALUES (:id, :cid, :plate, :type, :brand, :model, :fuel, :cap)"""),
            {"id": vid, "cid": company_id, "plate": plate, "type": vtype,
             "brand": brand, "model": model, "fuel": fuel, "cap": capacity},
        )

    driver_ids = []
    for name, lic in DRIVERS:
        did = str(uuid.uuid4())
        driver_ids.append(did)
        await db.execute(
            text("""INSERT INTO drivers (id, company_id, name, license_class)
                    VALUES (:id, :cid, :name, :lic)"""),
            {"id": did, "cid": company_id, "name": name, "lic": lic},
        )

    trip_count = 0
    for day_offset in range(90):
        trip_date = date.today() - timedelta(days=89 - day_offset)
        trips_this_day = random.randint(0, 3)
        for _ in range(trips_this_day):
            origin, destination, distance_km, base_revenue = random.choice(ROUTES)
            revenue = base_revenue * random.uniform(0.85, 1.15)
            vehicle_id = random.choice(vehicle_ids)
            driver_id = random.choice(driver_ids)
            customer_id = random.choice(customer_ids)
            trip_id = str(uuid.uuid4())
            departure = datetime.combine(trip_date, datetime.min.time()).replace(hour=random.randint(6, 14))
            arrival = departure + timedelta(hours=distance_km / 80)

            await db.execute(
                text("""INSERT INTO trips
                        (id, company_id, vehicle_id, driver_id, customer_id,
                         origin, destination, departure_at, arrival_at,
                         distance_km, revenue_eur, status)
                        VALUES (:id, :cid, :vid, :did, :custid,
                                :orig, :dest, :dep, :arr,
                                :dist, :rev, 'completed')"""),
                {"id": trip_id, "cid": company_id, "vid": vehicle_id, "did": driver_id,
                 "custid": customer_id, "orig": origin, "dest": destination,
                 "dep": departure, "arr": arrival, "dist": distance_km, "rev": round(revenue, 2)},
            )

            fuel_cost = distance_km * random.uniform(0.28, 0.38)
            await db.execute(
                text("""INSERT INTO fuel_costs (id, company_id, vehicle_id, trip_id, date, cost_eur, liters)
                        VALUES (:id, :cid, :vid, :tid, :date, :cost, :liters)"""),
                {"id": str(uuid.uuid4()), "cid": company_id, "vid": vehicle_id,
                 "tid": trip_id, "date": trip_date,
                 "cost": round(fuel_cost, 2), "liters": round(fuel_cost / 1.65, 1)},
            )

            toll_cost = distance_km * random.uniform(0.08, 0.18)
            await db.execute(
                text("""INSERT INTO operating_costs
                        (id, company_id, trip_id, category, description, amount_eur, date)
                        VALUES (:id, :cid, :tid, 'toll', 'Viapass', :amt, :date)"""),
                {"id": str(uuid.uuid4()), "cid": company_id, "tid": trip_id,
                 "amt": round(toll_cost, 2), "date": trip_date},
            )

            driver_hours = (arrival - departure).seconds / 3600
            salary_cost = driver_hours * random.uniform(18, 24)
            await db.execute(
                text("""INSERT INTO operating_costs
                        (id, company_id, trip_id, driver_id, category, description, amount_eur, date)
                        VALUES (:id, :cid, :tid, :did, 'salary', 'Driver hours', :amt, :date)"""),
                {"id": str(uuid.uuid4()), "cid": company_id, "tid": trip_id,
                 "did": driver_id, "amt": round(salary_cost, 2), "date": trip_date},
            )

            if random.random() < 0.08:
                maint_cost = random.uniform(80, 400)
                await db.execute(
                    text("""INSERT INTO operating_costs
                            (id, company_id, vehicle_id, category, description, amount_eur, date)
                            VALUES (:id, :cid, :vid, 'maintenance', 'Service/repair', :amt, :date)"""),
                    {"id": str(uuid.uuid4()), "cid": company_id, "vid": vehicle_id,
                     "amt": round(maint_cost, 2), "date": trip_date},
                )
            trip_count += 1

    for vehicle_id in vehicle_ids:
        await db.execute(
            text("""INSERT INTO operating_costs
                    (id, company_id, vehicle_id, category, description, amount_eur, date)
                    VALUES (:id, :cid, :vid, 'insurance', 'Monthly insurance', :amt, :date)"""),
            {"id": str(uuid.uuid4()), "cid": company_id, "vid": vehicle_id,
             "amt": round(random.uniform(280, 420), 2), "date": date.today().replace(day=1)},
        )

    await db.commit()
    return {"status": "seeded", "company_id": company_id, "trips_created": trip_count}
