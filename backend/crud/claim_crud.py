from sqlalchemy.orm import Session
from models.claim import Claim
from models.incentive import Incentive
from typing import Optional, List
from fastapi import HTTPException
from datetime import datetime

def submit_claim(db: Session, salesman_id: int, remarks: Optional[str] = None) -> Optional[Claim]:
    """
    Create a claim for all unclaimed incentives for a given salesman.
    Marks them as claimed and stores a claim record.
    """
    incentives = db.query(Incentive).filter_by(salesman_id=salesman_id, claimed=False).all()
    if not incentives:
        return None

    total_amount = sum(i.amount for i in incentives)

    # Mark all incentives as claimed
    for incentive in incentives:
        incentive.claimed = True

    claim = Claim(
        salesman_id=salesman_id,
        total_amount=total_amount,
        is_approved=False,
        remarks=remarks
    )

    try:
        db.add(claim)
        db.commit()
        db.refresh(claim)
    except Exception as e:
        db.rollback()
        raise e

    return claim


def get_all_claims(db: Session) -> List[Claim]:
    """
    Return all submitted claims sorted by newest first.
    """
    return db.query(Claim).order_by(Claim.timestamp.desc()).all()


def approve_claim_by_id(db: Session, claim_id: int) -> Optional[Claim]:
    """
    Approves the given claim. Returns updated claim, or None if not found.
    """
    claim = db.query(Claim).filter_by(id=claim_id).first()
    if not claim:
        return None

    claim.is_approved = True
    claim.updated_at = datetime.utcnow()

    try:
        db.commit()
        db.refresh(claim)
    except Exception as e:
        db.rollback()
        raise e

    return claim


def reject_claim_by_id(db: Session, claim_id: int) -> dict:
    """
    Rejects a claim by setting its status to 'rejected'.
    """
    claim = db.query(Claim).filter_by(id=claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim.status = "rejected"
    claim.updated_at = datetime.utcnow()

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return {"message": "Claim rejected"}


def amend_claim(db: Session, claim_id: int, new_remarks: str) -> dict:
    """
    Update the remarks of a claim.
    """
    claim = db.query(Claim).filter_by(id=claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    claim.remarks = new_remarks
    claim.updated_at = datetime.utcnow()

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise e

    return {"message": "Claim updated", "new_remarks": new_remarks}


def get_claim_by_id(db: Session, claim_id: int) -> Claim:
    """
    Retrieve a claim by its ID.
    """
    claim = db.query(Claim).filter_by(id=claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim
