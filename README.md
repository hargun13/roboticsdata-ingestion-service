# Robotics Telemetry Data Ingestion Service

Building a robotics telemetry data ingestion service with industrial equipment support.

## 1. Project Overview & Architecture

This project simulates a data ingestion pipeline for robotic and industrial equipment. It acts as a lightweight "Data Historian" interface, collecting time-series telemetry data from physical equipment and making it queryable for researchers building digital twins and AI models.

### Architecture
```text
[ Physical World ]          [ Ingestion Service ]           [ Storage Layer ]
Yaskawa Robot Arms  --->    FastAPI (Python)      --->    PostgreSQL Database
Autonomous AMRs             (Validates & Routes)          (Time-Series Storage)
```

**Design Decisions:**
1. **Decoupled Architecture:** Physical equipment only needs to know how to send HTTP POST requests; it is isolated from database logic.
2. **Payload Validation:** FastAPI enforces data integrity (e.g., ensuring torque is a float) before it hits the database, preventing pipeline crashes.
3. **Time-Series Optimization:** PostgreSQL is used to store telemetry, modeling the behavior of a specialized data historian through indexed time-series tables.

---

## 2. Tech Stack

*   **Web Framework:** FastAPI (Asynchronous, self-documenting)
*   **Web Server:** Uvicorn (ASGI server)
*   **Database:** PostgreSQL
*   **ORM:** SQLAlchemy (for safe, maintainable database interactions)
*   **Testing:** Pytest & HTTPX (for integration testing)
*   **HTTP Client:** HTTPX (for async/sync HTTP requests)

---

## 3. Database Schema

The project uses two core tables for managing equipment and telemetry data:

### Equipment Table
Stores metadata about physical devices (robots, AMRs, sensors, etc.)

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key, auto-incrementing |
| `name` | String | Equipment name (indexed for fast lookups) |
| `equipment_type` | String | Type of equipment (e.g., "6-axis robot arm", "AMR") |
| `location` | String | Physical location of equipment |
| `created_at` | DateTime | Timestamp when equipment was registered |

**Indexes:** `id` (primary), `name` (single column)

### Telemetry Table
Stores time-series telemetry readings from equipment

| Column | Type | Description |
|--------|------|-------------|
| `id` | Integer | Primary key, auto-incrementing |
| `timestamp` | DateTime | When the reading was taken (defaults to now) |
| `equipment_id` | Integer | Foreign key to Equipment table |
| `sensor_tag` | String | Name of the sensor (e.g., "joint_1_angle", "motor_torque") |
| `value` | Float | Numerical sensor reading |

**Composite Index:** `idx_equipment_sensor_time` on (`equipment_id`, `sensor_tag`, `timestamp`)  
This enables fast queries like "get all joint_1_angle readings for robot X between time A and B"

---

## 4. API Endpoints

### Root Endpoint
```
GET /
```
Returns service status.

**Response:**
```json
{
  "status": "online",
  "message": "Welcome to the Robotics Telemetry API"
}
```

### Register Equipment
```
POST /equipment/
```
Register a new piece of equipment in the system.

**Request Body:**
```json
{
  "name": "Yaskawa Arm",
  "equipment_type": "6-axis industrial robot arm",
  "location": "Factory Floor 1"
}
```

**Response (200):**
```json
{
  "id": 1,
  "name": "Yaskawa Arm",
  "equipment_type": "6-axis industrial robot arm",
  "location": "Factory Floor 1",
  "created_at": "2026-04-26T14:30:00+00:00"
}
```

### Ingest Telemetry Data
```
POST /telemetry/
```
Submit a sensor reading from equipment. Equipment must exist before submitting telemetry.

**Request Body:**
```json
{
  "equipment_id": 1,
  "sensor_tag": "joint_1_angle",
  "value": 45.5,
  "timestamp": "2026-04-26T14:30:00+00:00"
}
```

**Response (200):**
```json
{
  "id": 1,
  "equipment_id": 1,
  "sensor_tag": "joint_1_angle",
  "value": 45.5,
  "timestamp": "2026-04-26T14:30:00+00:00"
}
```

**Errors:**
- `404 Not Found`: Equipment ID does not exist
- `422 Unprocessable Entity`: Invalid data types (e.g., value is not a float)

### Query Telemetry Data
```
GET /telemetry/{equipment_id}?limit=100
```
Retrieve the most recent telemetry readings for a specific equipment.

**Parameters:**
- `equipment_id` (path): ID of the equipment
- `limit` (query, default=100): Maximum number of readings to return

**Response (200):**
```json
[
  {
    "id": 10,
    "equipment_id": 1,
    "sensor_tag": "joint_1_angle",
    "value": 45.5,
    "timestamp": "2026-04-26T14:35:00+00:00"
  },
  {
    "id": 9,
    "equipment_id": 1,
    "sensor_tag": "joint_1_angle",
    "value": 42.3,
    "timestamp": "2026-04-26T14:34:30+00:00"
  }
]
```

---

## 5. Installation & Setup

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- Git

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone <repository-url>
cd robotics-ingestion-service
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Create a `.env` file in the project root:
```
DATABASE_URL=postgresql://username:password@localhost:5432/telemetry_db
```

### Step 4: Create Database Tables
```bash
python create_tables.py
```

Output:
```
Connecting to PostgreSQL...
Tables created successfully!
```

---

## 6. Running the Project

### Start the FastAPI Server
```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### Access the Interactive API Documentation
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Use Swagger UI to test all endpoints without writing code.

---

## 7. Usage Examples

### Example 1: Register Equipment via cURL
```bash
curl -X POST "http://localhost:8000/equipment/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Yaskawa Arm",
    "equipment_type": "6-axis industrial robot arm",
    "location": "Factory Floor 1"
  }'
```

### Example 2: Send Telemetry Data
```bash
curl -X POST "http://localhost:8000/telemetry/" \
  -H "Content-Type: application/json" \
  -d '{
    "equipment_id": 1,
    "sensor_tag": "joint_1_angle",
    "value": 125.5
  }'
```

### Example 3: Query Recent Data
```bash
curl "http://localhost:8000/telemetry/1?limit=10"
```

---

## 8. Testing

### Run All Tests
```bash
pytest -v
```

### Test Coverage
The project includes tests for:
- **API Documentation Availability** (`test_read_docs`): Verifies Swagger UI is accessible
- **Equipment Registration** (`test_create_equipment`): Tests valid equipment creation and data validation
- **Data Validation** (`test_create_bad_telemetry`): Ensures invalid telemetry is rejected with 422 status

### Example Test Output
```
tests/test_main.py::test_read_docs PASSED
tests/test_main.py::test_create_equipment PASSED
tests/test_main.py::test_create_bad_telemetry PASSED

===== 3 passed in 0.25s =====
```

---

## 9. Simulator

For development and testing, use the included simulator to generate realistic robot telemetry data:

```bash
python simulator.py
```

**What it does:**
- Generates 20 simulated telemetry readings
- Sends `joint_1_angle` readings between 10-180 degrees
- Submits data every 0.5 seconds to Equipment ID 1
- Useful for testing data ingestion and querying

**Note:** Make sure the FastAPI server is running and equipment with ID=1 exists before running the simulator.

Example output:
```
🚀 Starting Yaskawa Arm simulation for Equipment ID: 1...
Press CTRL+C to stop.

✅ Saved Data: joint_1_angle = 45.32 degrees
✅ Saved Data: joint_1_angle = 127.88 degrees
✅ Saved Data: joint_1_angle = 82.15 degrees
...
```

---

## 10. Project Structure

```
robotics-ingestion-service/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── database.py           # Database connection and session setup
│   ├── models.py             # SQLAlchemy ORM models (Equipment, Telemetry)
│   ├── schemas.py            # Pydantic data validation schemas
│   └── main.py               # FastAPI application and endpoints
├── tests/
│   ├── __init__.py
│   └── test_main.py          # Integration tests
├── create_tables.py          # Script to initialize database tables
├── simulator.py              # Robot telemetry simulator for testing
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── .env                      # Environment variables (not in repo)
```

---

## 11. Key Features

✅ **Type-Safe:** Pydantic schemas validate all incoming data  
✅ **Scalable:** Composite indexes optimize time-series queries  
✅ **RESTful:** Standard HTTP methods and status codes  
✅ **Auto-Documented:** FastAPI generates interactive API docs automatically  
✅ **Tested:** Integration tests ensure reliability  
✅ **Decoupled:** Equipment is isolated from database implementation  

---

## 12. Future Enhancements

- [ ] Add authentication/authorization for equipment
- [ ] Implement data aggregation endpoints (average, min, max over time windows)
- [ ] Add bulk telemetry ingestion for high-throughput scenarios
- [ ] Implement time-based data retention policies
- [ ] Add metrics and monitoring dashboards
- [ ] Support for different sensor data types (pressure, vibration, temperature)
- [ ] Implement pagination for large result sets

---


