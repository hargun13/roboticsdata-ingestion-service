Building a robotics telemetry data ingestion service

## 1. Project Overview & Architecture

This project simulates a data ingestion pipeline for the Mill 19 robotic workcell. It acts as a lightweight "Data Historian" interface, collecting time-series telemetry data from physical lab equipment and making it queryable for researchers building digital twins and AI models.

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

---

