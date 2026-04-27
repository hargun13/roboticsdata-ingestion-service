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

# endpoint 2: ingest telemetry data

# endpoint 3: querying the data

# endpoint 4: 