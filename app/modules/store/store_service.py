from decimal import Decimal
from uuid import uuid4

from sqlalchemy.orm import Session, joinedload

from app.core.enums.roles import RoleName
from app.core.exceptions import BadRequestException, NotFoundException
from app.models.cart import Cart, CartItem
from app.models.customer import Customer
from app.models.order import Order, OrderItem, OrderStatusHistory
from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.stock_transaction import StockTransaction
from app.models.order_return import OrderReturn
from app.shared.audit import write_audit_log
from datetime import datetime
from app.modules.auth.auth_repository import AuthRepository


class StoreService:
    @staticmethod
    def _customer(db: Session, user_id: int) -> Customer:
        user = AuthRepository.get_user_by_id(db, user_id)
        if user is None or user.role.name != RoleName.CUSTOMER:
            raise BadRequestException("A customer account is required.")
        customer = db.query(Customer).filter(Customer.user_id == user_id).first()
        if customer is None:
            customer = Customer(full_name=user.full_name, email=user.email, phone=user.phone or f"user-{user.id}", user_id=user.id)
            db.add(customer)
            db.flush()
        return customer

    @staticmethod
    def get_cart(db: Session, user_id: int) -> Cart:
        customer = StoreService._customer(db, user_id)
        cart = db.query(Cart).options(joinedload(Cart.items).joinedload(CartItem.product)).filter(Cart.customer_id == customer.id).first()
        if cart is None:
            cart = Cart(customer_id=customer.id)
            db.add(cart)
            db.commit()
            db.refresh(cart)
        return cart

    @staticmethod
    def cart_response(cart: Cart):
        items = []
        subtotal = Decimal("0.00")
        for item in cart.items:
            if not item.product or not item.product.is_active:
                continue
            line = item.quantity * item.product.selling_price
            subtotal += line
            items.append({"product_id": item.product_id, "name": item.product.name, "sku": item.product.sku, "quantity": item.quantity, "unit_price": item.product.selling_price, "subtotal": line})
        return {"items": items, "subtotal": subtotal}

    @staticmethod
    def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
        customer = StoreService._customer(db, user_id)
        product = db.query(Product).filter(Product.id == product_id, Product.is_active.is_(True)).first()
        if product is None:
            raise NotFoundException("Product not found.")
        if product.stock_quantity < quantity:
            raise BadRequestException("Requested quantity exceeds available stock.")
        cart = db.query(Cart).filter(Cart.customer_id == customer.id).first()
        if cart is None:
            cart = Cart(customer_id=customer.id)
            db.add(cart)
            db.flush()
        item = db.query(CartItem).filter(CartItem.cart_id == cart.id, CartItem.product_id == product_id).first()
        new_qty = quantity if item is None else item.quantity + quantity
        if new_qty > product.stock_quantity:
            raise BadRequestException("Cart quantity exceeds available stock.")
        if item is None:
            item = CartItem(cart_id=cart.id, product_id=product_id, quantity=quantity)
            db.add(item)
        else:
            item.quantity = new_qty
        db.commit()
        return StoreService.cart_response(StoreService.get_cart(db, user_id))

    @staticmethod
    def update_cart_item(
        db: Session,
        user_id: int,
        product_id: int,
        quantity: int,
    ):
        if quantity < 1:
            raise BadRequestException(
                "Cart quantity must be at least 1."
            )

        customer = StoreService._customer(db, user_id)

        product = (
            db.query(Product)
            .filter(
                Product.id == product_id,
                Product.is_active.is_(True),
            )
            .first()
        )

        if product is None:
            raise NotFoundException("Product not found.")

        if quantity > product.stock_quantity:
            raise BadRequestException(
                "Cart quantity exceeds available stock."
            )

        item = (
            db.query(CartItem)
            .join(Cart)
            .filter(
                Cart.customer_id == customer.id,
                CartItem.product_id == product_id,
            )
            .first()
        )

        if item is None:
            raise NotFoundException("Cart item not found.")

        item.quantity = quantity

        try:
            db.commit()
            return StoreService.cart_response(
                StoreService.get_cart(db, user_id)
            )
        except Exception:
            db.rollback()
            raise


    @staticmethod
    def remove_from_cart(db: Session, user_id: int, product_id: int):
        customer = StoreService._customer(db, user_id)
        item = db.query(CartItem).join(Cart).filter(Cart.customer_id == customer.id, CartItem.product_id == product_id).first()
        if item is None:
            raise NotFoundException("Cart item not found.")
        db.delete(item)
        db.commit()
        return StoreService.cart_response(StoreService.get_cart(db, user_id))

    @staticmethod
    def checkout(db: Session, user_id: int, data):
        customer = StoreService._customer(db, user_id)
        cart = db.query(Cart).filter(Cart.customer_id == customer.id).first()
        if cart is None:
            raise BadRequestException("Cart is empty.")
        items = db.query(CartItem).filter(CartItem.cart_id == cart.id).all()
        if not items:
            raise BadRequestException("Cart is empty.")

        subtotal = Decimal("0.00")
        try:
            order = Order(order_number=f"ORD-{uuid4().hex[:12].upper()}", customer_id=customer.id, status="Confirmed", payment_status="Pending", payment_method=data.payment_method, subtotal=Decimal("0.00"), discount=Decimal("0.00"), shipping_fee=data.shipping_fee, total_amount=Decimal("0.00"), delivery_name=data.delivery_name, delivery_phone=data.delivery_phone, delivery_address=data.delivery_address, delivery_city=data.delivery_city, notes=data.notes)
            db.add(order)
            db.flush()

            sale = Sale(customer_id=customer.id, invoice_number=f"WEB-{uuid4().hex[:12].upper()}", sale_date=__import__('datetime').date.today(), total_amount=Decimal("0.00"), discount=Decimal("0.00"), tax=Decimal("0.00"), grand_total=Decimal("0.00"), payment_status="Pending", remarks=f"Online order {order.order_number}")
            db.add(sale)
            db.flush()

            for cart_item in items:
                product = db.query(Product).filter(Product.id == cart_item.product_id).with_for_update().first()
                if product is None or not product.is_active:
                    raise NotFoundException("A product in the cart is no longer available.")
                if product.stock_quantity < cart_item.quantity:
                    raise BadRequestException(f"Insufficient stock for {product.name}.")
                line = product.selling_price * cart_item.quantity
                subtotal += line
                order.items.append(OrderItem(product_id=product.id, product_name=product.name, sku=product.sku, quantity=cart_item.quantity, unit_price=product.selling_price, subtotal=line))
                sale.items.append(SaleItem(product_id=product.id, quantity=cart_item.quantity, unit_price=product.selling_price, cost_price=product.purchase_price, subtotal=line))
                db.add(StockTransaction(product_id=product.id, transaction_type="OUT", quantity=cart_item.quantity, unit_price=product.selling_price, remarks=f"Online order {order.order_number}"))
                product.stock_quantity -= cart_item.quantity

            order.subtotal = subtotal
            order.total_amount = subtotal + data.shipping_fee
            sale.total_amount = subtotal
            sale.grand_total = subtotal
            order.status_history.append(OrderStatusHistory(status="Confirmed", note="Online order placed."))
            db.query(CartItem).filter(CartItem.cart_id == cart.id).delete(synchronize_session=False)
            db.commit()
            db.refresh(order)
            return order
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def get_order(db: Session, user_id: int, order_id: int):
        customer = StoreService._customer(db, user_id)
        order = db.query(Order).options(joinedload(Order.items), joinedload(Order.status_history)).filter(Order.id == order_id, Order.customer_id == customer.id).first()
        if order is None:
            raise NotFoundException("Order not found.")
        return order

    @staticmethod
    def get_orders(db: Session, user_id: int):
        customer = StoreService._customer(db, user_id)
        return db.query(Order).options(joinedload(Order.items)).filter(Order.customer_id == customer.id).order_by(Order.id.desc()).all()


    @staticmethod
    def get_management_orders(db: Session):
        return db.query(Order).options(joinedload(Order.items), joinedload(Order.status_history)).order_by(Order.id.desc()).all()

    @staticmethod
    def update_order_status(db: Session, order_id: int, status: str, note: str | None, tracking_number: str | None, user_id: int | None = None):
        allowed = {"Pending", "Confirmed", "Processing", "Packed", "Shipped", "Delivered", "Cancelled"}
        if status not in allowed:
            raise BadRequestException("Invalid order status.")
        order = (db.query(Order).options(joinedload(Order.status_history), joinedload(Order.items))
                 .filter(Order.id == order_id).with_for_update().first())
        if order is None:
            raise NotFoundException("Order not found.")
        if order.status in {"Cancelled", "Delivered", "Returned"} and status != order.status:
            raise BadRequestException("This order can no longer change status.")
        if status == "Cancelled" and order.status != "Cancelled":
            if order.status == "Delivered":
                raise BadRequestException("Delivered orders cannot be cancelled.")
            sale = db.query(Sale).filter(Sale.remarks == f"Online order {order.order_number}").with_for_update().first()
            for item in order.items:
                product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
                if product is not None:
                    product.stock_quantity += item.quantity
                    db.add(StockTransaction(product_id=product.id, transaction_type="IN", quantity=item.quantity, unit_price=item.unit_price, remarks=f"Order {order.order_number} cancelled"))
            if sale is not None:
                sale.is_voided = True
                sale.payment_status = "Pending"
            order.payment_status = "Refunded" if sale is not None and any(p.amount > 0 for p in sale.payments) else order.payment_status
        order.status = status
        if tracking_number is not None:
            order.tracking_number = tracking_number
        order.status_history.append(OrderStatusHistory(status=status, note=note))
        write_audit_log(db, user_id=user_id, action="ORDER_STATUS", entity="Order", entity_id=order.id, details={"status": status, "note": note})
        try:
            db.commit()
            db.refresh(order)
            return order
        except Exception:
            db.rollback()
            raise

    @staticmethod
    def request_return(db: Session, user_id: int, data):
        customer = StoreService._customer(db, user_id)
        order = db.query(Order).filter(Order.id == data.order_id, Order.customer_id == customer.id).first()
        if order is None:
            raise NotFoundException("Order not found.")
        if order.status != "Delivered":
            raise BadRequestException("Only delivered orders can be returned.")
        existing = db.query(OrderReturn).filter(OrderReturn.order_id == order.id, OrderReturn.status.in_(["Requested", "Approved", "Processing"])).first()
        if existing:
            raise BadRequestException("A return request already exists for this order.")
        request = OrderReturn(order_id=order.id, customer_id=customer.id, status="Requested", reason=data.reason, notes=data.notes, refund_amount=Decimal("0.00"))
        db.add(request)
        try:
            db.commit(); db.refresh(request)
            write_audit_log(db, user_id=user_id, action="RETURN_REQUESTED", entity="OrderReturn", entity_id=request.id, details={"order_id": order.id})
            db.commit()
            return request
        except Exception:
            db.rollback(); raise

    @staticmethod
    def get_returns(db: Session, user_id: int):
        customer = StoreService._customer(db, user_id)
        return db.query(OrderReturn).filter(OrderReturn.customer_id == customer.id).order_by(OrderReturn.id.desc()).all()

    @staticmethod
    def update_return_status(db: Session, return_id: int, status: str, notes: str | None, user_id: int | None = None):
        allowed = {"Requested", "Approved", "Rejected", "Refunded"}
        if status not in allowed:
            raise BadRequestException("Invalid return status.")
        request = db.query(OrderReturn).filter(OrderReturn.id == return_id).with_for_update().first()
        if request is None:
            raise NotFoundException("Return request not found.")
        if request.status in {"Rejected", "Refunded"} and status != request.status:
            raise BadRequestException("This return request is already finalized.")
        order = db.query(Order).filter(Order.id == request.order_id).with_for_update().first()
        if order is None:
            raise NotFoundException("Order not found.")
        if status == "Approved":
            request.refund_amount = order.total_amount
        elif status == "Refunded":
            request.refund_amount = order.total_amount
            request.resolved_at = datetime.utcnow()
            order.payment_status = "Refunded"
            if order.status != "Cancelled":
                sale = db.query(Sale).filter(Sale.remarks == f"Online order {order.order_number}").with_for_update().first()
                if sale is not None:
                    sale.is_voided = True
                    sale.payment_status = "Refunded"
                for item in order.items:
                    product = db.query(Product).filter(Product.id == item.product_id).with_for_update().first()
                    if product is not None:
                        product.stock_quantity += item.quantity
                        db.add(StockTransaction(product_id=product.id, transaction_type="IN", quantity=item.quantity, unit_price=item.unit_price, remarks=f"Return refund for order {order.order_number}"))
                order.status = "Returned"
                order.status_history.append(OrderStatusHistory(status="Returned", note="Order refunded and inventory restored."))
        elif status == "Rejected":
            request.resolved_at = datetime.utcnow()
        request.status = status
        if notes:
            request.notes = notes
        write_audit_log(db, user_id=user_id, action="RETURN_STATUS", entity="OrderReturn", entity_id=request.id, details={"status": status, "order_id": order.id})
        try:
            db.commit(); db.refresh(request); return request
        except Exception:
            db.rollback(); raise
