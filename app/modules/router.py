from fastapi import APIRouter

from app.modules.auth.auth_api import router as auth_router
from app.modules.categories.category_api import router as category_router
from app.modules.customers.customer_api import router as customer_router
from app.modules.dashboard.dashboard_api import router as dashboard_router
from app.modules.inventory.inventory_api import router as inventory_router
from app.modules.payments.payment_api import router as payment_router
from app.modules.products.product_api import router as product_router
from app.modules.purchases.purchase_api import router as purchase_router
from app.modules.reports.report_api import router as report_router
from app.modules.sales.sale_api import router as sale_router
from app.modules.suppliers.supplier_api import router as supplier_router
from app.modules.uploads.upload_api import router as upload_router
from app.modules.roles.role_api import router as role_router
from app.modules.users.user_api import router as user_router
from app.modules.permissions.permission_api import router as permission_router
from app.modules.store.store_api import router as store_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(category_router)
api_router.include_router(product_router)
api_router.include_router(inventory_router)
api_router.include_router(supplier_router)
api_router.include_router(purchase_router)
api_router.include_router(customer_router)
api_router.include_router(sale_router)
api_router.include_router(payment_router)
api_router.include_router(dashboard_router)
api_router.include_router(report_router)
api_router.include_router(upload_router)
api_router.include_router(role_router)
api_router.include_router(user_router)
api_router.include_router(permission_router)
api_router.include_router(store_router)
