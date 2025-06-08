from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ClaimOut(BaseModel):
    id: int
    salesman_id: int
    total_amount: float
    is_approved: bool
    remarks: Optional[str]
    timestamp: datetime

    # Extras for frontend
    salesman_name: Optional[str] = "Salesman"
    reason: Optional[str] = None

    class Config:
        orm_mode = True


class ClaimUpdateRequest(BaseModel):
    new_remarks: str
