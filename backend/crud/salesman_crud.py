from sqlalchemy.orm import Session
from models.salesman import Salesman
from schemas.salesman_schema import SalesmanCreate, SalesmanApprove
from utils.hash import hash_password, verify_password


def create_salesman(db: Session, data: SalesmanCreate) -> Salesman:
    """
    Create a new salesman. They are unapproved by default.
    Raises ValueError if mobile already exists.
    """
    existing = db.query(Salesman).filter_by(mobile=data.mobile).first()
    if existing:
        raise ValueError("Salesman with this mobile already exists")

    new_salesman = Salesman(
        name=data.name,
        mobile=data.mobile,
        outlet=data.outlet,
        is_approved=False
    )

    try:
        db.add(new_salesman)
        db.commit()
        db.refresh(new_salesman)
    except Exception as e:
        db.rollback()
        raise e

    return new_salesman


def get_pending_salesmen(db: Session) -> list[Salesman]:
    """
    Return all salesmen who have registered but are not yet approved.
    """
    return db.query(Salesman).filter_by(is_approved=False).all()


def approve_salesman(db: Session, salesman_id: int, data: SalesmanApprove) -> Salesman | None:
    """
    Approve a salesman and set their password, outlet, and category.
    Returns None if salesman not found.
    """
    salesman = db.query(Salesman).filter_by(id=salesman_id).first()
    if not salesman:
        return None

    if salesman.is_approved:
        return salesman  # Already approved

    salesman.outlet = data.outlet
    salesman.category = data.category
    salesman.password = hash_password(data.password)
    salesman.is_approved = True

    try:
        db.commit()
        db.refresh(salesman)
    except Exception as e:
        db.rollback()
        raise e

    return salesman


def login_salesman_by_credentials(db: Session, mobile: str, password: str) -> Salesman | None:
    """
    Authenticate a salesman by mobile and password.
    Returns the salesman if valid, else None.
    """
    salesman = db.query(Salesman).filter_by(mobile=mobile).first()
    if not salesman or not salesman.is_approved:
        return None

    if not verify_password(password, salesman.password):
        return None

    return salesman


def get_salesman_by_phone(db: Session, mobile: str) -> Salesman | None:
    """
    Fetch a salesman by mobile number. Used for auth validation.
    """
    return db.query(Salesman).filter_by(mobile=mobile).first()
