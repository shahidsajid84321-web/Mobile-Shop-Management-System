from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.modules.auth.dependencies import get_current_user
from app.modules.auth.auth_schema import UserRegister, UserResponse
from app.modules.auth.auth_service import AuthService
from app.models.user import User
from app.models.product import Product
from app.modules.categories.category_model import Category
from app.core.enums.roles import RoleName
from app.dependencies.role_dependency import require_roles
from app.modules.store.store_schema import (
    CartItemRequest, CartResponse, CheckoutRequest, OrderResponse, StoreProductResponse,
    StoreCategoryResponse, CustomerStoreProfileResponse, OrderStatusUpdate,
)
from app.modules.store.store_service import StoreService
from app.modules.store.return_schema import ReturnCreate, ReturnResponse, ReturnStatusUpdate
from app.shared.common_schema import ApiResponse
from app.shared.responses import success_response

router = APIRouter(prefix="/store", tags=["Online Store"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register_customer(data: UserRegister, db: Session = Depends(get_db)):
    return AuthService.register_user(db=db, user_data=data)



@router.get("/categories", response_model=ApiResponse[list[StoreCategoryResponse]])
def public_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).order_by(Category.name.asc()).all()
    return success_response("Store categories retrieved successfully.", categories)


@router.get("/products", response_model=ApiResponse[list[StoreProductResponse]])
def public_products(db: Session = Depends(get_db)):
    items = db.query(Product).filter(Product.is_active.is_(True)).order_by(Product.id.desc()).all()
    return success_response("Store products retrieved successfully.", items)


@router.get("/products/{product_id}", response_model=ApiResponse[StoreProductResponse])
def public_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.is_active.is_(True)).first()
    if product is None:
        from app.core.exceptions import NotFoundException
        raise NotFoundException("Product not found.")
    return success_response("Store product retrieved successfully.", product)


@router.get("/me", response_model=ApiResponse[CustomerStoreProfileResponse])
def store_me(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return success_response("Customer profile retrieved successfully.", StoreService._customer(db, current_user.id))


@router.get("/cart", response_model=ApiResponse[CartResponse])
def get_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return success_response("Cart retrieved successfully.", StoreService.cart_response(StoreService.get_cart(db, current_user.id)))


@router.post("/cart/items", response_model=ApiResponse[CartResponse], status_code=201)
def add_cart_item(data: CartItemRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return success_response("Item added to cart successfully.", StoreService.add_to_cart(db, current_user.id, data.product_id, data.quantity))


@router.delete("/cart/items/{product_id}", response_model=ApiResponse[CartResponse])
def remove_cart_item(product_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return success_response("Item removed from cart successfully.", StoreService.remove_from_cart(db, current_user.id, product_id))


@router.patch(
    "/cart/items/{product_id}",
    response_model=ApiResponse[CartResponse],
)
def update_cart_item(
    product_id: int,
    data: CartItemRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return success_response(
        "Cart item updated successfully.",
        StoreService.update_cart_item(
            db,
            current_user.id,
            product_id,
            data.quantity,
        ),
    )


@router.post("/checkout", response_model=ApiResponse[OrderResponse], status_code=201)
def checkout(data: CheckoutRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return success_response("Order placed successfully.", StoreService.checkout(db, current_user.id, data))


@router.get("/orders", response_model=ApiResponse[list[OrderResponse]])
def get_orders(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return success_response("Orders retrieved successfully.", StoreService.get_orders(db, current_user.id))


@router.get("/orders/{order_id}", response_model=ApiResponse[OrderResponse])
def get_order(order_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return success_response("Order retrieved successfully.", StoreService.get_order(db, current_user.id, order_id))


@router.get("/management/orders", response_model=ApiResponse[list[OrderResponse]])
def management_orders(db: Session = Depends(get_db), current_user: User = Depends(require_roles(RoleName.SUPER_ADMIN, RoleName.ADMIN, RoleName.MANAGER))):
    return success_response("Online orders retrieved successfully.", StoreService.get_management_orders(db))


@router.patch("/management/orders/{order_id}/status", response_model=ApiResponse[OrderResponse])
def update_order_status(order_id: int, data: OrderStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_roles(RoleName.SUPER_ADMIN, RoleName.ADMIN, RoleName.MANAGER))):
    return success_response("Order status updated successfully.", StoreService.update_order_status(db, order_id, data.status, data.note, data.tracking_number))


@router.post("/returns", response_model=ApiResponse[ReturnResponse], status_code=201)
def request_return(data: ReturnCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return success_response("Return request created successfully.", StoreService.request_return(db, current_user.id, data))

@router.get("/returns", response_model=ApiResponse[list[ReturnResponse]])
def get_returns(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return success_response("Return requests retrieved successfully.", StoreService.get_returns(db, current_user.id))

@router.patch("/management/returns/{return_id}/status", response_model=ApiResponse[ReturnResponse])
def update_return_status(return_id: int, data: ReturnStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_roles(RoleName.SUPER_ADMIN, RoleName.ADMIN, RoleName.MANAGER))):
    return success_response("Return request updated successfully.", StoreService.update_return_status(db, return_id, data.status, data.notes, current_user.id))
