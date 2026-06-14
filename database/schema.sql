-- LogiFlow PostgreSQL Schema
-- Belgium-focused logistics profitability analytics

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Companies (tenants)
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    vat_number VARCHAR(20),
    country CHAR(2) NOT NULL DEFAULT 'BE',
    city VARCHAR(100),
    plan_tier VARCHAR(20) NOT NULL DEFAULT 'free' CHECK (plan_tier IN ('free', 'starter', 'growth', 'enterprise')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    google_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- User → Company membership
CREATE TABLE user_companies (
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL DEFAULT 'viewer' CHECK (role IN ('admin', 'manager', 'viewer')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (user_id, company_id)
);

-- Customers (clients of the transport company)
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    city VARCHAR(100),
    country CHAR(2) DEFAULT 'BE',
    vat_number VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- Drivers
CREATE TABLE drivers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    license_class VARCHAR(10),
    license_expiry DATE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- Vehicles
CREATE TABLE vehicles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    plate VARCHAR(20) NOT NULL,
    type VARCHAR(50),
    brand VARCHAR(100),
    model VARCHAR(100),
    year INTEGER,
    fuel_type VARCHAR(20) CHECK (fuel_type IN ('diesel', 'petrol', 'electric', 'hybrid', 'cng', 'lpg')),
    capacity_kg NUMERIC(10, 2),
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ,
    UNIQUE (company_id, plate)
);

-- Trips
CREATE TABLE trips (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    vehicle_id UUID REFERENCES vehicles(id),
    driver_id UUID REFERENCES drivers(id),
    customer_id UUID REFERENCES customers(id),
    origin VARCHAR(255) NOT NULL,
    destination VARCHAR(255) NOT NULL,
    departure_at TIMESTAMPTZ,
    arrival_at TIMESTAMPTZ,
    distance_km NUMERIC(10, 2),
    weight_kg NUMERIC(10, 2),
    revenue_eur NUMERIC(12, 2) NOT NULL DEFAULT 0,
    status VARCHAR(20) NOT NULL DEFAULT 'completed' CHECK (status IN ('planned', 'in_progress', 'completed', 'cancelled')),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMPTZ
);

-- Fuel costs (per vehicle fill-up)
CREATE TABLE fuel_costs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    vehicle_id UUID NOT NULL REFERENCES vehicles(id) ON DELETE CASCADE,
    trip_id UUID REFERENCES trips(id),
    date DATE NOT NULL,
    liters NUMERIC(8, 2),
    cost_eur NUMERIC(10, 2) NOT NULL,
    odometer_km NUMERIC(10, 2),
    station VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Operating costs (tolls, maintenance, salaries, insurance, etc.)
CREATE TABLE operating_costs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    trip_id UUID REFERENCES trips(id),
    vehicle_id UUID REFERENCES vehicles(id),
    driver_id UUID REFERENCES drivers(id),
    category VARCHAR(50) NOT NULL CHECK (category IN ('toll', 'maintenance', 'salary', 'insurance', 'admin', 'other')),
    description VARCHAR(255),
    amount_eur NUMERIC(12, 2) NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Invoices
CREATE TABLE invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
    customer_id UUID REFERENCES customers(id),
    trip_id UUID REFERENCES trips(id),
    invoice_number VARCHAR(100),
    amount_eur NUMERIC(12, 2) NOT NULL,
    vat_eur NUMERIC(12, 2) DEFAULT 0,
    issued_at DATE NOT NULL,
    due_at DATE,
    paid_at DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'draft' CHECK (status IN ('draft', 'sent', 'paid', 'overdue', 'cancelled')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Route performance (materialized view — refreshed nightly or on demand)
CREATE MATERIALIZED VIEW route_performance AS
SELECT
    t.company_id,
    t.origin,
    t.destination,
    COUNT(t.id) AS trip_count,
    ROUND(AVG(t.revenue_eur)::numeric, 2) AS avg_revenue_eur,
    ROUND(AVG(
        COALESCE(fc.fuel_per_trip, 0) + COALESCE(oc.cost_per_trip, 0)
    )::numeric, 2) AS avg_cost_eur,
    ROUND(AVG(t.distance_km)::numeric, 2) AS avg_distance_km,
    MIN(t.departure_at) AS first_trip_at,
    MAX(t.departure_at) AS last_trip_at
FROM trips t
LEFT JOIN (
    SELECT trip_id, SUM(cost_eur) AS fuel_per_trip
    FROM fuel_costs
    WHERE trip_id IS NOT NULL
    GROUP BY trip_id
) fc ON fc.trip_id = t.id
LEFT JOIN (
    SELECT trip_id, SUM(amount_eur) AS cost_per_trip
    FROM operating_costs
    WHERE trip_id IS NOT NULL
    GROUP BY trip_id
) oc ON oc.trip_id = t.id
WHERE t.deleted_at IS NULL AND t.status = 'completed'
GROUP BY t.company_id, t.origin, t.destination;

CREATE UNIQUE INDEX ON route_performance (company_id, origin, destination);

-- Indexes for common query patterns
CREATE INDEX idx_trips_company_id ON trips(company_id);
CREATE INDEX idx_trips_departure_at ON trips(departure_at);
CREATE INDEX idx_trips_customer_id ON trips(customer_id);
CREATE INDEX idx_trips_vehicle_id ON trips(vehicle_id);
CREATE INDEX idx_trips_driver_id ON trips(driver_id);
CREATE INDEX idx_fuel_costs_vehicle_id ON fuel_costs(vehicle_id);
CREATE INDEX idx_fuel_costs_date ON fuel_costs(date);
CREATE INDEX idx_operating_costs_company_id ON operating_costs(company_id);
CREATE INDEX idx_operating_costs_date ON operating_costs(date);
CREATE INDEX idx_invoices_company_id ON invoices(company_id);
CREATE INDEX idx_invoices_customer_id ON invoices(customer_id);
CREATE INDEX idx_invoices_status ON invoices(status);
CREATE INDEX idx_customers_company_id ON customers(company_id);
CREATE INDEX idx_vehicles_company_id ON vehicles(company_id);
CREATE INDEX idx_drivers_company_id ON drivers(company_id);
