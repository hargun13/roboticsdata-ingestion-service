from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Connection String for PostgreSQL
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

if not SQLALCHEMY_DATABASE_URL:
	raise ValueError("DATABASE_URL environment variable is not set")

# The engine is the core interface to the db, it manages the connection pool
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session for your db workspace actions
# autocommit=False means that you have to commit your transactions manually, which is good for ensuring data integrity
# autoflush=False means that changes to the session won't be automatically flushed to the database until you explicitly call flush() or commit()
# bind=engine tells the session to use the engine we created for database interactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class should be inherited from the declarative base for your models
# This is a common pattern in SQLAlchemy where you define a base class that your models will inherit from, allowing SQLAlchemy to keep track of all the models and their relationships
Base = declarative_base()