from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.payment import Payment
from app.modules.payments.payment_repository import PaymentRepository
from app.modules.payments.payment_schema import PaymentCreate
from app.modules.sales.sale_repository import SaleRepository


class PaymentService:

    @staticmethod
    def create(
        db: Session,
        data: PaymentCreate,
    ):

        sale = SaleRepository.get_by_id(
            db,
            data.sale_id,
        )

        if sale is None:
            raise ValueError("Sale not found.")

        total_paid = Decimal("0.00")

        for payment in sale.payments:
            total_paid += payment.amount

        if total_paid + data.amount > sale.grand_total:
            raise ValueError("Payment exceeds remaining balance.")

        payment = Payment(
            sale_id=data.sale_id,
            amount=data.amount,
            payment_method=data.payment_method,
            payment_date=data.payment_date,
            reference_number=data.reference_number,
            remarks=data.remarks,
        )

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

    @staticmethod
    def get_all(
        db: Session,
    ):
        return PaymentRepository.get_all(db)

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
            raise ValueError("Payment not found.")

        return payment
