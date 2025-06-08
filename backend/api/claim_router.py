from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from db.database import get_db
from crud.claim_crud import (
    submit_claim,
    get_all_claims,
    approve_claim_by_id,
    reject_claim_by_id,
    amend_claim,
    get_claim_by_id
)
from schemas.claim_schema import ClaimOut, ClaimUpdateRequest
from utils.security import get_current_user_role
from models.claim import Claim

router = APIRouter(prefix="/api/claims", tags=["Claims"])


# 🚹 Salesman submits a claim for unclaimed incentives
@router.post("/submit", response_model=ClaimOut)
def submit_incentive_claim(
    remarks: Optional[str] = None,
    db: Session = Depends(get_db),
    salesman=Depends(get_current_user_role("salesman"))
):
    claim = submit_claim(db, salesman_id=salesman.id, remarks=remarks)
    if not claim:
        raise HTTPException(status_code=404, detail="No unclaimed incentives available.")
    return claim


# 👑 Admin views all submitted claims
@router.get("/", response_model=list[ClaimOut])
def list_all_claims(
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    return get_all_claims(db)


# 👑 Admin views only unapproved (pending) claims
@router.get("/pending", response_model=list[ClaimOut])
def get_pending_claims(
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    return db.query(Claim).filter_by(is_approved=False).all()


# 👑 Admin approves a claim
@router.post("/approve/{claim_id}", response_model=ClaimOut)
def approve_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    claim = approve_claim_by_id(db, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found.")
    return claim


# 👑 Admin rejects a claim
@router.post("/reject/{claim_id}")
def reject_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    success = reject_claim_by_id(db, claim_id)
    if not success:
        raise HTTPException(status_code=404, detail="Claim not found or already handled.")
    return {"message": "Claim rejected successfully."}


# 👑 Admin amends claim remarks
@router.post("/amend/{claim_id}")
def amend_claim_remarks(
    claim_id: int,
    payload: ClaimUpdateRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    updated_claim = amend_claim(db, claim_id, payload.new_remarks)
    if not updated_claim:
        raise HTTPException(status_code=404, detail="Claim not found.")
    return {"message": "Remarks updated successfully."}


# 👑 Admin gets specific claim by ID
@router.get("/{claim_id}", response_model=ClaimOut)
def get_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    claim = get_claim_by_id(db, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found.")
    return claim
