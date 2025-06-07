from sqlalchemy.orm import Session
from models.sale import Sale
from schemas.sale_schema import SaleSubmit


def submit_sale(db: Session, sale: SaleSubmit, salesman_id: int) -> Sale:
    """
    Insert a new sale entry for the given salesman.
    """
    new_sale = Sale(
        barcode=sale.barcode,
        customer_number=sale.customer_number,
        salesman_id=salesman_id
    )

    try:
        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)
    except Exception as e:
        db.rollback()
        raise e

    return new_sale


def get_sales_by_salesman(db: Session, salesman_id: int) -> list[Sale]:
    """
    Return all sales entered by a specific salesman.
    """
    return db.query(Sale).filter_by(salesman_id=salesman_id).all()
