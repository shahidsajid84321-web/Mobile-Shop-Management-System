from datetime import date
from decimal import Decimal

from sqlalchemy import Date, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import TimestampMixin


class Sale(Base, TimestampMixin):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    invoice_number: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    sale_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    discount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    tax: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
    )

    grand_total: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    payment_status: Mapped[str] = mapped_column(
        String(30),
        default="Pending",
    )

    remarks: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    customer = relationship(
        "Customer",
        back_populates="sales",
    )

    items = relationship(
        "SaleItem",
        back_populates="sale",
        cascade="all, delete-orphan",
    )

    payments = relationship(
        "Payment",
        back_populates="sale",
        cascade="all, delete-orphan",
    )    