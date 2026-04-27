from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

# We import the tools we built in the previous steps!
from app import models, schemas
from app.database import engine, SessionLocal


# Initiate the FastAPI app
app = FastAPI()

# db dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"status": "online", "message": "Welcome to the Robotics Telemetry API"}

# endpoint 1: register new equipment
@app.post("/equipment/", response_model=schemas.EquipmentResponse)
def create_equipment(equipment: schemas.EquipmentCreate, db: Session = Depends(get_db)):
    # 1. Pydantic validation done
    # 2. We convert the Pydantic schema into a SQLAlchemy Database Model
    # equipment.model_dump() converts the Pydantic model into a dictionary, and ** unpacks that dictionary into keyword arguments for the SQLAlchemy model constructor
    db_equipment = models.Equipment(**equipment.model_dump())
    
    # 3. We add it to the database workspace, commit it to the hard drive, and refresh the object to get its new ID.
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    
    # 4. We return the saved object. FastAPI automatically converts it back to JSON
    return db_equipment

# endpoint 2: ingest telemetry data
@app.post("/telemetry/", response_model=schemas.TelemetryResponse)
def create_telemetry(telemetry: schemas.TelemetryCreate, db: Session = Depends(get_db)):
    
    # Security check: Does this robot actually exist in our database?
    equipment = db.query(models.Equipment).filter(models.Equipment.id == telemetry.equipment_id).first()
    if not equipment:
        # If not, FastAPI instantly returns a 404 Not Found error to the robot.
        raise HTTPException(status_code=404, detail="Equipment not found")
    
    # Save the telemetry point
    db_telemetry = models.Telemetry(**telemetry.model_dump())
    db.add(db_telemetry)
    db.commit()
    db.refresh(db_telemetry)
    return db_telemetry

# endpoint 3: querying the data (for the researchers)
@app.get("/telemetry/{equipment_id}", response_model=List[schemas.TelemetryResponse])
def get_telemetry(equipment_id: int, limit: int = 100, db: Session = Depends(get_db)):
    
    # Query the database for this specific robot's data, ordered by the newest first.
    # Because we added that composite index in models.py, this query is lightning fast!
    readings = db.query(models.Telemetry)\
                 .filter(models.Telemetry.equipment_id == equipment_id)\
                 .order_by(models.Telemetry.timestamp.desc())\
                 .limit(limit)\
                 .all()
    
    return readings