from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime
from datetime import datetime
from backend.db.database import Base

class Incentive(Base):
    __tablename__ = "incentives"

    id = Column(Integer, primary_key=True, index=True)
    salesman_id = Column(Integer, ForeignKey("salesmen.id"))
    barcode = Column(String)
    amount = Column(Float)  # calculated
    trait = Column(String)
    is_visible = Column(Boolean, default=True)  # if hidden by admin, don't show
    timestamp = Column(DateTime, default=datetime.utcnow)
