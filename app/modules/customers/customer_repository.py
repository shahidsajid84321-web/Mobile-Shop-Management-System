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
    def get_paginated(
        db: Session,
        page: int,
        page_size: int,
    ) -> tuple[list[Customer], int]:

        query = (
            db.query(Customer)
            .order_by(Customer.id.desc())
        )

        total = query.count()

        offset = (page - 1) * page_size

        customers = (
            query
            .offset(offset)
            .limit(page_size)
            .all()
        )

        return customers, total

    @staticmethod
    def get_by_id(
        db: Session,
        customer_id: int,
    ):

        return db.query(Customer).filter(Customer.id == customer_id).first()

    @staticmethod
    def get_by_phone(
        db: Session,
        phone: str,
    ):

        return db.query(Customer).filter(Customer.phone == phone).first()

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ):
        return db.query(Customer).filter(Customer.email == email).first()

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
