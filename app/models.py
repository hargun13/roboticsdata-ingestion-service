# Schemas for the database models
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Index
from sqlalchemy.sql import func
from app.database import Base

class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    equipment_type = Column(String)
    location = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())

class Telemetry(Base):
    __tablename__ = "telemetry"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), default=func.now())
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    sensor_tag = Column(String, nullable=False)
    value = Column(Float, nullable=False)

    # Composite Indexes for efficient querying
    # Example: give me the data for equipment x between time a and time b
    # A composite index will speed up these queries to find this exact combination instantly
    __table_args__ = (
        Index('idx_equipment_sensor_time', 'equipment_id', 'sensor_tag', 'timestamp'),
    )
