import uuid
from datetime import datetime, date
from sqlalchemy import String, DateTime, Date, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    company_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("companies.id"), nullable=False)
    customer_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("customers.id"))
    trip_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("trips.id"))
    invoice_number: Mapped[str | None] = mapped_column(String(100))
    amount_eur: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    vat_eur: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    issued_at: Mapped[date] = mapped_column(Date, nullable=False)
    due_at: Mapped[date | None] = mapped_column(Date)
    paid_at: Mapped[date | None] = mapped_column(Date)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
