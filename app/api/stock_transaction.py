from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db

from app.schemas.stock_transaction_schema import (
    StockTransactionCreate,
    StockTransactionResponse,
)

from app.services.stock_transaction_service import (
    StockTransactionService,
)

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.post(
    "/",
    response_model=StockTransactionResponse,
    status_code=201,
)
def create_transaction(
    transaction: StockTransactionCreate,
    db: Session = Depends(get_db),
):
    try:
        return StockTransactionService.create(
            db,
            transaction,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[StockTransactionResponse],
)
def get_transactions(
    db: Session = Depends(get_db),
):
    return StockTransactionService.get_all(db)


@router.get(
    "/product/{product_id}",
    response_model=list[StockTransactionResponse],
)
def get_product_transactions(
    product_id: int,
    db: Session = Depends(get_db),
):
    return StockTransactionService.get_by_product(
        db,
        product_id,
    )