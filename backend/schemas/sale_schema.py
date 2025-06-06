from pydantic import BaseModel
from typing import Optional
class SaleSubmit(BaseModel):
    barcode: str
    customer_number: str
    salesman_id: Optional[int] = None
class SaleOut(BaseModel):
    id: int
    barcode: str
    customer_number: str

    class Config:
        from_attributes = True
