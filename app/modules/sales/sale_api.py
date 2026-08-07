from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.dependencies.db import get_db
from app.modules.sales.sale_schema import SaleCreate, SaleResponse
from app.modules.sales.sale_service import SaleService

router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


@router.post(
    "/",
    response_model=SaleResponse,
    status_code=201,
)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
):
    try:
        return SaleService.create(
            db,
            sale,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[SaleResponse],
)
def get_sales(
    db: Session = Depends(get_db),
):
    return SaleService.get_all(db)


@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
):
    try:
        return SaleService.get_one(
            db,
            sale_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )
