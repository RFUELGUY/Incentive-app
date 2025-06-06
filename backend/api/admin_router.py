# incentive-app/backend/api/admin_router.py

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.db.database import SessionLocal
from backend.models.admin import Admin
from backend.utils.security import (
    get_current_user_role,
    hash_password,
    MASTER_ADMIN_SECRET
)
from backend.crud.admin_crud import get_admin_by_phone

router = APIRouter(prefix="/admin", tags=["Admin"])

# -------------------------------
# DB Dependency
# -------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------------
# 🔐 Secure Test Ping (Admin Only)
# -------------------------------
@router.get("/ping")
def ping_admin(admin=Depends(get_current_user_role("admin"))):
    """
    Admin: Test route to confirm admin access.
    """
    return {"status": "admin router active", "admin": admin.phone}

# -------------------------------
# 🔐 Admin Creation via Master Key
# -------------------------------
class AdminCreateRequest(BaseModel):
    name: str
    phone: str
    password: str
    master_key: str

@router.post("/create", status_code=201)
def create_admin(payload: AdminCreateRequest, db: Session = Depends(get_db)):
    """
    One-time Admin creation endpoint protected by MASTER_ADMIN_SECRET.
    """
    if payload.master_key != MASTER_ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Invalid master key")

    if get_admin_by_phone(db, payload.phone):
        raise HTTPException(status_code=409, detail="Admin already exists")

    new_admin = Admin(
        name=payload.name,
        phone=payload.phone,
        hashed_password=hash_password(payload.password),
        is_active=True
    )

    try:
        db.add(new_admin)
        db.commit()
        db.refresh(new_admin)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Admin creation failed: {str(e)}")

    return {"message": "✅ Admin created", "phone": new_admin.phone}
