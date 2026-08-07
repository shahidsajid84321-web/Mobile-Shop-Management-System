from sqlalchemy.orm import Session

from app.models.customer import Customer


class CustomerRepository:

    @staticmethod
    def create(
        db: Session,
        customer: Customer,
    ) -> Customer:

        db.add(customer)
        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def get_all(
        db: Session,
    ):

        return db.query(Customer).all()

    @staticmethod
    def get_by_id(
        db: Session,
        customer_id: int,
    ):

        return (
            db.query(Customer)
            .filter(Customer.id == customer_id)
            .first()
        )

    @staticmethod
    def get_by_phone(
        db: Session,
        phone: str,
    ):

        return (
            db.query(Customer)
            .filter(Customer.phone == phone)
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        customer: Customer,
    ) -> Customer:

        db.commit()
        db.refresh(customer)

        return customer

    @staticmethod
    def delete(
        db: Session,
        customer: Customer,
    ):

        db.delete(customer)
        db.commit()