from fastapi import FastAPI

from app.core.config import settings
from app.modules.auth.auth_api import router as auth_router
from app.api.product import router as product_router
from app.modules.categories.categories_api import router as categories_router
from app.api.supplier import router as supplier_router
from app.api.purchase import router as purchase_router
from app.api.customer import router as customer_router
from app.api.sale import router as sale_router
from app.api.payment import router as payment_router
from app.api.dashboard import router as dashboard_router
from app.api.report import router as report_router
from fastapi.staticfiles import StaticFiles
from app.api.upload import router as upload_router

from app.core.exception_handlers import (
    register_exception_handlers,
)

from app.api.stock_transaction import (
    router as stock_transaction_router,
)


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.mount(
    "/uploads",
    StaticFiles(directory="app/uploads"),
    name="uploads",
)

app.include_router(auth_router)
app.include_router(product_router)
app.include_router(categories_router)
app.include_router(stock_transaction_router)
app.include_router(supplier_router)
app.include_router(purchase_router)
app.include_router(customer_router)
app.include_router(sale_router)
app.include_router(payment_router)
app.include_router(dashboard_router)
app.include_router(report_router)
app.include_router(upload_router)

register_exception_handlers(app)

@app.get("/")
def root():
    return {
        "project": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug": settings.DEBUG,
    }