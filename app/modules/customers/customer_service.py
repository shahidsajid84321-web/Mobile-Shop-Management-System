from sqlalchemy.orm import Session

from app.core.exceptions import BadRequestException, NotFoundException
from app.shared.pagination import PaginatedResponse
from app.models.customer import Customer
from app.modules.customers.customer_repository import CustomerRepository
from app.modules.customers.customer_schema import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)


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
            raise BadRequestException("Phone number already exists.")

        if data.email and CustomerRepository.get_by_email(db, data.email):
            raise BadRequestException("Email already exists.")

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
        page: int,
        page_size: int,
    ) -> PaginatedResponse[CustomerResponse]:

        customers, total = CustomerRepository.get_paginated(
            db,
            page,
            page_size,
        )

        return PaginatedResponse.create(
            items=customers,
            page=page,
            page_size=page_size,
            total=total,
        )

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

        phone_owner = CustomerRepository.get_by_phone(db, data.phone)
        if phone_owner and phone_owner.id != customer.id:
            raise BadRequestException("Phone number already exists.")
        if data.email:
            email_owner = CustomerRepository.get_by_email(db, data.email)
            if email_owner and email_owner.id != customer.id:
                raise BadRequestException("Email already exists.")

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

        if customer.sales:
            raise BadRequestException("Customer cannot be deleted because sales are recorded for it.")

        CustomerRepository.delete(
            db,
            customer,
        )
