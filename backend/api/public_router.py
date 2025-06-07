from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import SessionLocal
from models.outlet import Outlet

router = APIRouter(prefix="/public", tags=["Public"])

# --- DB Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Public: List outlets for signup ---
@router.get("/outlets", response_model=list[dict])
def list_public_outlets(db: Session = Depends(get_db)):
    return [{"id": o.id, "name": o.name} for o in db.query(Outlet).all()]