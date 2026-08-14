from decimal import Decimal
from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field


from app.modules.auth.auth_schema import UserRegister


class StoreCategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    model_config = ConfigDict(from_attributes=True)


class StoreProductResponse(BaseModel):
    id: int
    name: str
    brand: str
    model_number: str | None
    sku: str
    description: str | None
    selling_price: Decimal
    stock_quantity: int
    image: str | None
    category_id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class CartItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, le=1000)


class CartItemResponse(BaseModel):
    product_id: int
    name: str
    sku: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal


class CartResponse(BaseModel):
    items: list[CartItemResponse]
    subtotal: Decimal


class CheckoutRequest(BaseModel):
    delivery_name: str = Field(min_length=2, max_length=100)
    delivery_phone: str = Field(min_length=7, max_length=20)
    delivery_address: str = Field(min_length=5, max_length=500)
    delivery_city: str = Field(min_length=2, max_length=100)
    payment_method: str = Field(default="Cash on Delivery", min_length=2, max_length=30)
    shipping_fee: Decimal = Field(default=Decimal("0.00"), ge=0)
    notes: str | None = Field(default=None, max_length=500)


class CustomerOrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    sku: str
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    model_config = ConfigDict(from_attributes=True)


class OrderStatusHistoryResponse(BaseModel):
    status: str
    note: str | None
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class OrderResponse(BaseModel):
    id: int
    order_number: str
    status: str
    payment_status: str
    payment_method: str
    subtotal: Decimal
    discount: Decimal
    shipping_fee: Decimal
    total_amount: Decimal
    delivery_name: str
    delivery_phone: str
    delivery_address: str
    delivery_city: str
    tracking_number: str | None
    notes: str | None
    placed_at: datetime
    items: list[CustomerOrderItemResponse]
    status_history: list[OrderStatusHistoryResponse]
    model_config = ConfigDict(from_attributes=True)


class CustomerStoreProfileResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr | None
    phone: str
    address: str | None
    model_config = ConfigDict(from_attributes=True)


class OrderStatusUpdate(BaseModel):
    status: str = Field(min_length=2, max_length=30)
    note: str | None = Field(default=None, max_length=500)
    tracking_number: str | None = Field(default=None, max_length=100)
