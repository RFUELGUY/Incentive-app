from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ClaimRequest(BaseModel):
    remarks: Optional[str] = None

class ClaimOut(BaseModel):
    id: int
    salesman_id: int
    total_amount: float
    is_approved: bool
    remarks: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True
