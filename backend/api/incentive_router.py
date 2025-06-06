# incentive-app/backend/api/incentive_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.database import SessionLocal
from backend.schemas.incentive_schema import IncentiveOut
from backend.schemas.claim_schema import ClaimRequest, ClaimOut
from backend.crud.claim_crud import (
    get_all_claims,
    submit_claim,
    approve_claim_by_id
)
from backend.crud.incentive_crud import (
    get_incentives_for_salesman,
    
    generate_incentives
)
from backend.utils.security import get_current_user_role

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/my-incentives", response_model=list[IncentiveOut])
def get_my_incentives(
    db: Session = Depends(get_db),
    salesman=Depends(get_current_user_role("salesman"))
):
    """
    Salesman: Fetch all visible incentives for logged-in user.
    """
    return get_incentives_for_salesman(db, salesman.id)

@router.post("/claim", response_model=ClaimOut)
def claim_incentive(
    payload: ClaimRequest,
    db: Session = Depends(get_db),
    salesman=Depends(get_current_user_role("salesman"))
):
    """
    Salesman: Submit claim for eligible incentives.
    """
    claim = submit_claim(db, salesman.id, remarks=payload.remarks)
    if not claim:
        raise HTTPException(status_code=404, detail="No unclaimed incentives found.")
    return claim

@router.get("/claims", response_model=list[ClaimOut])
def all_claims(
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    """
    Admin: View all submitted claims.
    """
    return get_all_claims(db)

@router.post("/approve-claim", response_model=ClaimOut)
def approve_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    """
    Admin: Approve a specific claim.
    """
    claim = approve_claim_by_id(db, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim

@router.post("/generate")
def generate(
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    """
    Admin: Trigger incentive generation.
    """
    return generate_incentives(db)
