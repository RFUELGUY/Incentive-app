# backend/api/leaderboard_router.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from db.database import SessionLocal
from crud.leaderboard_crud import get_leaderboard, calculate_leaderboard
from pydantic import BaseModel

class StreakUpdate(BaseModel):
    user_id: int
    date: str  # e.g., "2025-06-07"
router = APIRouter(prefix="/api", tags=["Leaderboard"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/leaderboard")
def leaderboard_view(
    scope: str = Query(..., regex="^(day|week|month)$"),
    db: Session = Depends(get_db)
):
    """
    Get top performers based on scope: day/week/month.
    """
    return get_leaderboard(db, scope)


# backend/api/leaderboard_router.py (continued)

from pydantic import BaseModel

class StreakUpdate(BaseModel):
    user_id: int
    date: str  # e.g., "2025-06-07"

@router.post("/streaks/update")
def update_streak(data: StreakUpdate, db: Session = Depends(get_db)):
    """
    Update or extend sales streak for a given user on a date.
    """
    from crud.leaderboard_crud import update_user_streak
    return update_user_streak(db, data.user_id, data.date)

@router.get("/leaderboard/streak")
def leaderboard_streak(db: Session = Depends(get_db)):
    from crud.leaderboard_crud import get_streak_leaderboard
    return get_streak_leaderboard(db)


router = APIRouter()

@router.get("/day")
def leaderboard_day(db: Session = Depends(get_db)):
    return calculate_leaderboard(db, period="day")

@router.get("/week")
def leaderboard_week(db: Session = Depends(get_db)):
    return calculate_leaderboard(db, period="week")

@router.get("/month")
def leaderboard_month(db: Session = Depends(get_db)):
    return calculate_leaderboard(db, period="month")

@router.get("/streak")
def leaderboard_streak(db: Session = Depends(get_db)):
    return calculate_leaderboard(db, period="streak")