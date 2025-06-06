from sqlalchemy.orm import Session
from backend.models.claim import Claim
from backend.models.incentive import Incentive
from typing import Optional


def submit_claim(db: Session, salesman_id: int, remarks: Optional[str] = None) -> Optional[Claim]:
    """
    Create a claim for all unclaimed incentives for a given salesman.
    Marks them as claimed and stores a claim record.
    Returns the created claim or None if no incentives were found.
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


def get_all_claims(db: Session) -> list[Claim]:
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

    try:
        db.commit()
        db.refresh(claim)
    except Exception as e:
        db.rollback()
        raise e

    return claim
