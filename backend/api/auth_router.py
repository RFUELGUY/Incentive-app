# incentive-app/backend/api/auth_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from schemas.salesman_schema import (
    SalesmanCreate,
    SalesmanLogin,
    SalesmanOut,
    SalesmanApprove,
)
from crud.salesman_crud import (
    create_salesman,
    get_pending_salesmen,
    approve_salesman,
    get_salesman_by_phone,
)
from crud.admin_crud import get_admin_by_phone
from utils.security import (
    verify_password,
    create_access_token,
    get_current_user_role,
)
from db.database import SessionLocal

# 🔥 Removed internal prefix to avoid /api/auth/auth duplication
router = APIRouter(tags=["Authentication"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------- Signup Route (Salesman Only) -----------

@router.post("/signup", response_model=SalesmanOut)
def signup(salesman: SalesmanCreate, db: Session = Depends(get_db)):
    """
    Public: Register a new salesman (is_approved=False by default).
    """
    return create_salesman(db, salesman)


# ----------- Admin Only: View Pending Signups -----------

@router.get("/pending", response_model=list[SalesmanOut])
def list_pending(db: Session = Depends(get_db), admin=Depends(get_current_user_role("admin"))):
    """
    Admin Only: List all unapproved salesmen.
    """
    return get_pending_salesmen(db)


# ----------- Admin Only: Approve Salesman -----------

@router.post("/approve/{salesman_id}", response_model=SalesmanOut)
def approve(
    salesman_id: int,
    data: SalesmanApprove,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin")),
):
    """
    Admin Only: Approve a salesman and set password, category, and outlet.
    """
    approved = approve_salesman(db, salesman_id, data)
    if not approved:
        raise HTTPException(status_code=404, detail="Salesman not found")
    return approved


# ----------- Shared Login Endpoint (Admin / Salesman) -----------

class LoginRequest(BaseModel):
    mobile: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    # Try admin
    user = get_admin_by_phone(db, payload.mobile)
    if user and verify_password(payload.password, user.hashed_password):
        token = create_access_token({"sub": user.mobile, "role": "admin"})
        return {"access_token": token, "token_type": "bearer", "role": "admin"}

    # Try salesman
    user = get_salesman_by_phone(db, payload.mobile)
    if user and user.is_approved and verify_password(payload.password, user.hashed_password):
        token = create_access_token({"sub": user.mobile, "role": "salesman"})
        return {"access_token": token, "token_type": "bearer", "role": "salesman"}

    raise HTTPException(status_code=401, detail="Invalid credentials or not approved")