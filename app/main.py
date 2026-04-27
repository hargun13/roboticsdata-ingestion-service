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

# endpoint 1: register new equipment
@app.post("/equipment/", response_model=schemas.EquipmentResponse)
def create_equipment(equipment: schemas.EquipmentCreate, db: Session = Depends(get_db)):
    
    # 1. Pydantic validation done
    # 2. We convert the Pydantic schema into a SQLAlchemy Database Model
    db_equipment = models.Equipment(**equipment.model_dump())
    
    # 3. We add it to the database workspace, commit it to the hard drive, and refresh the object to get its new ID.
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    
    # 4. We return the saved object. FastAPI automatically converts it back to JSON
    return db_equipment

# endpoint 2: ingest telemetry data



# endpoint 3: querying the data

# endpoint 4: 