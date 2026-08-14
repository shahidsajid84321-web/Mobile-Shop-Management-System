from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.core.exceptions import BadRequestException, NotFoundException
from app.modules.payments.payment_repository import PaymentRepository
from app.modules.payments.payment_schema import PaymentCreate
from app.modules.sales.sale_repository import SaleRepository
from app.shared.pagination import PaginationParams, PaginatedResponse


class PaymentService:

    @staticmethod
    def create(
        db: Session,
        data: PaymentCreate,
    ):
        sale = SaleRepository.get_by_id_for_update(
            db,
            data.sale_id,
        )

        if sale is None:
            raise NotFoundException("Sale not found.")

        total_paid = Decimal("0.00")

        for payment in sale.payments:
            total_paid += payment.amount

        remaining_balance = sale.grand_total - total_paid

        if remaining_balance <= Decimal("0.00"):
            raise BadRequestException(
                "Sale has no remaining payment balance."
            )

        if data.amount > remaining_balance:
            raise BadRequestException(
                "Payment exceeds remaining balance."
            )

        payment = Payment(
            sale_id=data.sale_id,
            amount=data.amount,
            payment_method=data.payment_method,
            payment_date=data.payment_date,
            reference_number=data.reference_number,
            remarks=data.remarks,
        )

        try:
            PaymentRepository.create(
                db,
                payment,
            )

            total_paid += data.amount

            if total_paid == sale.grand_total:
                sale.payment_status = "Paid"

            elif total_paid > Decimal("0.00"):
                sale.payment_status = "Partial"

            else:
                sale.payment_status = "Pending"

            db.commit()
            db.refresh(payment)

            return payment

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_all(
        db: Session,
        pagination: PaginationParams,
    ) -> PaginatedResponse[Payment]:
        items, total = PaymentRepository.get_all(
            db, pagination.page, pagination.page_size
        )
        return PaginatedResponse.create(
            items=items,
            page=pagination.page,
            page_size=pagination.page_size,
            total=total,
        )

    @staticmethod
    def get_one(
        db: Session,
        payment_id: int,
    ):
        payment = PaymentRepository.get_by_id(
            db,
            payment_id,
        )

        if payment is None:
            raise NotFoundException("Payment not found.")

        return payment
