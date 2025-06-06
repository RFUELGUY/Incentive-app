from sqlalchemy.orm import Session
from backend.models.admin import Admin
from backend.utils.hash import hash_password



def get_admin_by_phone(db: Session, phone: str) -> Admin | None:
    """
    Fetch admin by registered phone number.
    """
    return db.query(Admin).filter(Admin.phone == phone).first()


def is_admin_active(admin: Admin) -> bool:
    """
    Check if admin account is active.
    """
    return bool(admin and admin.is_active)


def create_admin(db: Session, name: str, phone: str, password: str) -> Admin:
    """
    Create a new admin with hashed password.
    Raises if phone is already registered.
    """
    existing = get_admin_by_phone(db, phone)
    if existing:
        raise ValueError("Admin with this phone already exists.")

    new_admin = Admin(
        name=name,
        phone=phone,
        hashed_password=hash_password(password),
        is_active=True
    )

    try:
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
    except Exception as e:
        db.rollback()
        raise e

    return new_admin
