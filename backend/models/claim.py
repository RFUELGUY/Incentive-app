from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.db.database import Base

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    salesman_id = Column(Integer, ForeignKey("salesmen.id"), nullable=False)
    total_amount = Column(Float, nullable=False)
    is_approved = Column(Boolean, default=False)
    remarks = Column(String, nullable=True)

    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    salesman = relationship("Salesman", back_populates="claims")
