from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException
from app.models.customer import Customer
from app.modules.customers.customer_repository import CustomerRepository
from app.modules.customers.customer_schema import (CustomerCreate,
                                                   CustomerUpdate)


class CustomerService:

    @staticmethod
    def create(
        db: Session,
        data: CustomerCreate,
    ):

        existing = CustomerRepository.get_by_phone(
            db,
            data.phone,
        )

        if existing:
            raise ValueError("Phone number already exists.")

        customer = Customer(
            full_name=data.full_name,
            email=data.email,
            phone=data.phone,
            address=data.address,
        )

        return CustomerRepository.create(
            db,
            customer,
        )

    @staticmethod
    def get_all(
        db: Session,
    ):
        return CustomerRepository.get_all(db)

    @staticmethod
    def get_one(
        db: Session,
        customer_id: int,
    ):

        customer = CustomerRepository.get_by_id(
            db,
            customer_id,
        )

        if customer is None:
            raise NotFoundException("Customer not found.")

        return customer

    @staticmethod
    def update(
        db: Session,
        customer_id: int,
        data: CustomerUpdate,
    ):

        customer = CustomerRepository.get_by_id(
            db,
            customer_id,
        )

        if customer is None:
            raise NotFoundException("Customer not found.")

        customer.full_name = data.full_name
        customer.email = data.email
        customer.phone = data.phone
        customer.address = data.address
        customer.is_active = data.is_active

        return CustomerRepository.update(
            db,
            customer,
        )

    @staticmethod
    def delete(
        db: Session,
        customer_id: int,
    ):

        customer = CustomerRepository.get_by_id(
            db,
            customer_id,
        )

        if customer is None:
            raise NotFoundException("Customer not found.")

        CustomerRepository.delete(
            db,
            customer,
        )
