# this file tells fastapi what kind of data we expect from the robots
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# Incoming data from robots
class EquipmentCreate(BaseModel):
    name: str
    equipment_type: str
    location: Optional[str] = None

class TelemetryCreate(BaseModel):
    equipment_id: int
    sensor_tag: str
    value: float
    timestamp: Optional[datetime] = None  # if not provided, we can set it to now in the endpoint

# Outgoing data to clients
class EquipmentResponse(BaseModel):
    id: int
    name: str
    equipment_type: str
    location: Optional[str] = None
    created_at: datetime

    class Config:
        # this tells pydantic to read data from the ORM models directly
        from_attributes = True

class TelemetryResponse(BaseModel):
    id: int
    equipment_id: int
    sensor_tag: str
    value: float
    timestamp: datetime

    class Config:
        from_attributes = True