from app.database import engine, Base
from app.models import Equipment, Telemetry

print("Connecting to PostgreSQL...")
# This command looks at our models.py and translates them into SQL CREATE TABLE commands
Base.metadata.create_all(bind=engine)
print("Tables created successfully in mfi_ddb!")