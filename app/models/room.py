# app/models/room.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Room(Base):
    __tablename__ = "Room"
    
    BuildingCode = Column(String(10), ForeignKey("Building.BuildingCode"), primary_key=True)
    RoomNumber = Column(Integer, primary_key=True)
    RoomType = Column(String(50), nullable=True)

    # Relationship back to Building
    building = relationship("Building", back_populates="rooms")
