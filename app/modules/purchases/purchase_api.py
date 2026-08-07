from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.modules.purchases.purchase_schema import (PurchaseCreate,
                                                   PurchaseResponse)
from app.modules.purchases.purchase_service import PurchaseService

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"],
)


@router.post(
    "/",
    response_model=PurchaseResponse,
    status_code=201,
)
def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db),
):
    try:
        return PurchaseService.create(
            db,
            purchase,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[PurchaseResponse],
)
def get_purchases(
    db: Session = Depends(get_db),
):
    return PurchaseService.get_all(db)


@router.get(
    "/{purchase_id}",
    response_model=PurchaseResponse,
)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
):
    try:
        return PurchaseService.get_one(
            db,
            purchase_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
