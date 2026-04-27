# Principle: Arrange, Act, Assert
# fastapi provides a TestClient so we can directly use that and use pytest to run our tests
from fastapi.testclient import TestClient
from app.main import app

# Arrange
client = TestClient(app)

# Act
# test read docs if they are online or not
def test_read_docs():
    # Act
    response = client.get("/docs")
    # Assert
    assert response.status_code == 200

# test to create new equipment
def test_create_equipment():
    # Arrange fake data
    payload = {
        "name": "Yaskawa Arm",
        "equipment_type": "A 6-axis industrial robot arm used for precision tasks in manufacturing.",
        "location": "Factory Floor 1"
    }
    # Act
    response = client.post("/equipment/", json=payload)

    # Assert
    assert response.status_code == 200

    # check if api echoed back our data correctly
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["equipment_type"] == payload["equipment_type"]
    assert data["location"] == payload["location"] 
    assert "id" in data #to check if id was generated and returned

def test_create_bad_telemetry():
    # Arrange fake telemetry data with non-existent equipment_id
    bad_payload = {
        "equipment_id": 9999, # Assuming this ID does not exist in the database
        "sensor_tag": "joint_1_angle",
        "value": "this should be a number, but it's a string" # Invalid value type
    }
    # Act
    response = client.post("/telemetry/", json=bad_payload)

    # Assert
    assert response.status_code == 422
