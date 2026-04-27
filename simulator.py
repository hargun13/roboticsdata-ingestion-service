import httpx
import time
import random

# The URL of your local FastAPI server
API_URL = "http://localhost:8000"

# We assume the robot you just created in the Swagger UI got ID = 1
EQUIPMENT_ID = 1 

def simulate_robot_data():
    print(f"🚀 Starting Yaskawa Arm simulation for Equipment ID: {EQUIPMENT_ID}...")
    print("Press CTRL+C to stop.\n")
    
    # Create a synchronous HTTP client to send requests
    with httpx.Client() as client:
        try:
            for i in range(20): # We will send 20 data points
                # 1. Generate fake telemetry data
                payload = {
                    "equipment_id": EQUIPMENT_ID,
                    "sensor_tag": "joint_1_angle",
                    "value": round(random.uniform(10.0, 180.0), 2) # Random angle between 10 and 180
                }
                
                # 2. Send the POST request to your API
                response = client.post(f"{API_URL}/telemetry/", json=payload)
                
                # 3. Print the result so we can watch it happen
                if response.status_code == 200:
                    print(f"✅ Saved Data: {payload['sensor_tag']} = {payload['value']} degrees")
                else:
                    print(f"❌ Error: {response.json()}")
                
                # Wait half a second before sending the next data point
                time.sleep(0.5)
                
        except KeyboardInterrupt:
            print("\n🛑 Simulation stopped by user.")

if __name__ == "__main__":
    simulate_robot_data()