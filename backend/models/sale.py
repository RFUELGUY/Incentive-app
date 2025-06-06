from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from backend.db.database import Base
from datetime import datetime
class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String, nullable=False)
    customer_number = Column(String, nullable=False)
    salesman_id = Column(Integer, ForeignKey("salesmen.id"), nullable=False)

    # Optional: if you want backref from Salesman
    salesman = relationship("Salesman", back_populates="sales")
    timestamp = Column(DateTime, default=datetime.utcnow)