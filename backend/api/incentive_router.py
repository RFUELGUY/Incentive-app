# incentive-app/backend/api/incentive_router.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from schemas.incentive_schema import IncentiveOut
from schemas.claim_schema import ClaimRequest, ClaimOut
from crud.incentive_crud import (
    toggle_incentive_visibility,
    get_incentives_for_salesman,
    generate_incentives,
    get_all_incentives
)
from crud.claim_crud import (
    get_all_claims,
    submit_claim,
    approve_claim_by_id
)
from utils.security import get_current_user_role

router = APIRouter()

# DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ Salesman: View visible incentives
@router.get("/my-incentives", response_model=list[IncentiveOut])
def get_my_incentives(
    db: Session = Depends(get_db),
    salesman=Depends(get_current_user_role("salesman"))
):
    return get_incentives_for_salesman(db, salesman.id)


# ✅ Salesman: Submit claim
@router.post("/claim", response_model=ClaimOut)
def claim_incentive(
    payload: ClaimRequest,
    db: Session = Depends(get_db),
    salesman=Depends(get_current_user_role("salesman"))
):
    claim = submit_claim(db, salesman.id, remarks=payload.remarks)
    if not claim:
        raise HTTPException(status_code=404, detail="No unclaimed incentives found.")
    return claim


# ✅ Admin: View all claims
@router.get("/claims", response_model=list[ClaimOut])
def all_claims(
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    return get_all_claims(db)


# ✅ Admin: Approve claim
@router.post("/approve-claim", response_model=ClaimOut)
def approve_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    claim = approve_claim_by_id(db, claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim


# ✅ Admin: Trigger generation of incentives
@router.post("/generate")
def generate(
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    return generate_incentives(db)


# ✅ Admin: View all incentives
@router.get("/", response_model=list[IncentiveOut])
def get_all(
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    return get_all_incentives(db)


# ✅ Admin: Toggle visibility of an incentive
@router.patch("/incentives/{incentive_id}/visibility")
def update_visibility(
    incentive_id: int,
    data: dict,
    db: Session = Depends(get_db),
    admin=Depends(get_current_user_role("admin"))
):
    is_visible = data.get("is_visible")
    if is_visible is None:
        raise HTTPException(status_code=400, detail="Missing visibility flag.")
    try:
        updated = toggle_incentive_visibility(db, incentive_id, is_visible)
        return {"message": "Visibility updated", "incentive_id": updated.id}
    except ValueError:
        raise HTTPException(status_code=404, detail="Incentive not found")
