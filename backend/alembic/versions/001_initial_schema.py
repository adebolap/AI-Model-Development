"""initial schema

Revision ID: 001
Revises:
Create Date: 2026-06-14

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    op.create_table(
        'companies',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('vat_number', sa.String(20)),
        sa.Column('country', sa.String(2), nullable=False, server_default='BE'),
        sa.Column('city', sa.String(100)),
        sa.Column('plan_tier', sa.String(20), nullable=False, server_default='free'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('google_id', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('avatar_url', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('google_id'),
        sa.UniqueConstraint('email'),
    )

    op.create_table(
        'customers',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255)),
        sa.Column('phone', sa.String(50)),
        sa.Column('city', sa.String(100)),
        sa.Column('country', sa.String(2), server_default='BE'),
        sa.Column('vat_number', sa.String(20)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'drivers',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('email', sa.String(255)),
        sa.Column('phone', sa.String(50)),
        sa.Column('license_class', sa.String(10)),
        sa.Column('license_expiry', sa.Date()),
        sa.Column('active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'vehicles',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('plate', sa.String(20), nullable=False),
        sa.Column('type', sa.String(50)),
        sa.Column('brand', sa.String(100)),
        sa.Column('model', sa.String(100)),
        sa.Column('year', sa.Integer()),
        sa.Column('fuel_type', sa.String(20)),
        sa.Column('capacity_kg', sa.Numeric(10, 2)),
        sa.Column('active', sa.Boolean(), server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.UniqueConstraint('company_id', 'plate'),
    )

    op.create_table(
        'trips',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('vehicle_id', postgresql.UUID(as_uuid=True)),
        sa.Column('driver_id', postgresql.UUID(as_uuid=True)),
        sa.Column('customer_id', postgresql.UUID(as_uuid=True)),
        sa.Column('origin', sa.String(255), nullable=False),
        sa.Column('destination', sa.String(255), nullable=False),
        sa.Column('departure_at', sa.DateTime(timezone=True)),
        sa.Column('arrival_at', sa.DateTime(timezone=True)),
        sa.Column('distance_km', sa.Numeric(10, 2)),
        sa.Column('weight_kg', sa.Numeric(10, 2)),
        sa.Column('revenue_eur', sa.Numeric(12, 2), server_default='0'),
        sa.Column('status', sa.String(20), server_default='completed'),
        sa.Column('notes', sa.Text()),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('deleted_at', sa.DateTime(timezone=True)),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id']),
        sa.ForeignKeyConstraint(['driver_id'], ['drivers.id']),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id']),
    )

    op.create_table(
        'fuel_costs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('vehicle_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('trip_id', postgresql.UUID(as_uuid=True)),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('liters', sa.Numeric(8, 2)),
        sa.Column('cost_eur', sa.Numeric(10, 2), nullable=False),
        sa.Column('odometer_km', sa.Numeric(10, 2)),
        sa.Column('station', sa.String(100)),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['vehicle_id'], ['vehicles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['trip_id'], ['trips.id']),
    )

    op.create_table(
        'operating_costs',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('trip_id', postgresql.UUID(as_uuid=True)),
        sa.Column('vehicle_id', postgresql.UUID(as_uuid=True)),
        sa.Column('driver_id', postgresql.UUID(as_uuid=True)),
        sa.Column('category', sa.String(50), nullable=False),
        sa.Column('description', sa.String(255)),
        sa.Column('amount_eur', sa.Numeric(12, 2), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
    )

    op.create_table(
        'invoices',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('uuid_generate_v4()'), nullable=False),
        sa.Column('company_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('customer_id', postgresql.UUID(as_uuid=True)),
        sa.Column('trip_id', postgresql.UUID(as_uuid=True)),
        sa.Column('invoice_number', sa.String(100)),
        sa.Column('amount_eur', sa.Numeric(12, 2), nullable=False),
        sa.Column('vat_eur', sa.Numeric(12, 2), server_default='0'),
        sa.Column('issued_at', sa.Date(), nullable=False),
        sa.Column('due_at', sa.Date()),
        sa.Column('paid_at', sa.Date()),
        sa.Column('status', sa.String(20), server_default='draft'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id']),
        sa.ForeignKeyConstraint(['trip_id'], ['trips.id']),
    )

    op.create_index('idx_trips_company_id', 'trips', ['company_id'])
    op.create_index('idx_trips_departure_at', 'trips', ['departure_at'])
    op.create_index('idx_trips_customer_id', 'trips', ['customer_id'])
    op.create_index('idx_trips_vehicle_id', 'trips', ['vehicle_id'])
    op.create_index('idx_invoices_company_id', 'invoices', ['company_id'])
    op.create_index('idx_invoices_status', 'invoices', ['status'])
    op.create_index('idx_customers_company_id', 'customers', ['company_id'])
    op.create_index('idx_vehicles_company_id', 'vehicles', ['company_id'])
    op.create_index('idx_drivers_company_id', 'drivers', ['company_id'])


def downgrade() -> None:
    op.drop_table('invoices')
    op.drop_table('operating_costs')
    op.drop_table('fuel_costs')
    op.drop_table('trips')
    op.drop_table('vehicles')
    op.drop_table('drivers')
    op.drop_table('customers')
    op.drop_table('users')
    op.drop_table('companies')
