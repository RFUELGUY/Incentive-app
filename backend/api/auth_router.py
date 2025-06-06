# incentive-app/backend/api/auth_router.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.schemas.salesman_schema import (
    SalesmanCreate,
    SalesmanLogin,
    SalesmanOut,
    SalesmanApprove,
)
from backend.crud.salesman_crud import (
    create_salesman,
    get_pending_salesmen,
    approve_salesman,
    get_salesman_by_phone,
)
from backend.crud.admin_crud import get_admin_by_phone
from backend.utils.security import (
    verify_password,
    create_access_token,
    get_current_user_role,
)
from backend.db.database import SessionLocal

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----- Signup / Approval Flow -----

@router.post("/signup", response_model=SalesmanOut)
def signup(salesman: SalesmanCreate, db: Session = Depends(get_db)):
    """
    Register a new salesman (unapproved by default).
    """
    return create_salesman(db, salesman)

@router.get("/pending", response_model=list[SalesmanOut])
def list_pending(db: Session = Depends(get_db), admin=Depends(get_current_user_role("admin"))):
    """
    Admin: List all unapproved salesmen.
    """
    return get_pending_salesmen(db)

@router.post("/approve/{salesman_id}", response_model=SalesmanOut)
def approve(salesman_id: int, data: SalesmanApprove, db: Session = Depends(get_db), admin=Depends(get_current_user_role("admin"))):
    """
    Admin: Approve a salesman by ID and set category, outlet, and password.
    """
    approved = approve_salesman(db, salesman_id, data)
    if not approved:
        raise HTTPException(status_code=404, detail="Salesman not found")
    return approved

# ----- Login + Token Flow -----

class LoginRequest(BaseModel):
    phone: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """
    Login for either Admin or Approved Salesman using phone + password.
    Returns JWT token.
    """
    # Try admin
    user = get_admin_by_phone(db, payload.phone)
    if user and verify_password(payload.password, user.hashed_password):
        token = create_access_token({"sub": user.phone, "role": "admin"})
        return {"access_token": token, "token_type": "bearer"}

    # Try salesman
    user = get_salesman_by_phone(db, payload.phone)
    if user and user.is_approved and verify_password(payload.password, user.hashed_password):
        token = create_access_token({"sub": user.phone, "role": "salesman"})
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Invalid credentials or not approved")
