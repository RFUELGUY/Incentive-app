# incentive-app/backend/api/sales_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.schemas.sale_schema import SaleSubmit, SaleOut
from backend.crud.sale_crud import submit_sale, get_sales_by_salesman
from backend.db.database import SessionLocal
from backend.utils.security import get_current_user_role

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/submit", response_model=SaleOut)
def create_sale(
    sale: SaleSubmit,
    db: Session = Depends(get_db),
    salesman=Depends(get_current_user_role("salesman"))
):
    """
    Salesman: Submit a sale entry.
    """
    sale.salesman_id = salesman.id
    return submit_sale(db, sale)

@router.get("/my-sales", response_model=list[SaleOut])
def my_sales(
    db: Session = Depends(get_db),
    salesman=Depends(get_current_user_role("salesman"))
):
    """
    Salesman: View my submitted sales.
    """
    return get_sales_by_salesman(db, salesman.id)
