# app/models/building.py
from sqlalchemy import Column, String, Integer, DECIMAL
from sqlalchemy.orm import relationship
from app.core.database import Base

class Building(Base):
    __tablename__ = "Building"

    BuildingCode = Column(String(10), primary_key=True, index=True)
    Name = Column(String(100), nullable=False)
    YearBuilt = Column(Integer, nullable=True)   # YEAR stored as Integer
    Cost = Column(DECIMAL(12, 2), nullable=True)

    # Relationships
    rooms = relationship("Room", back_populates="building")