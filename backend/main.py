from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
import os

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", "8000"))
NODE_TIMEOUT_SECONDS = int(os.getenv("NODE_TIMEOUT_SECONDS", "5"))

app = FastAPI(title="SIH26025 Mine Monitoring API")


latest_data = {}


@app.get("/")
def root():
    return {
        "project": "SIH26025",
        "status": "running"
    }


@app.post("/api/sensor")
def receive_sensor_data(data: dict):
    node_id = data.get("node_id", "UNKNOWN")

    latest_data[node_id] = data

    print("\n========== SENSOR DATA ==========")
    print(data)

    return {
        "status": "success",
        "node_id": node_id
    }


@app.get("/api/sensor/{node_id}")
def get_sensor_data(node_id: str):
    return latest_data.get(
        node_id,
        {"error": "Node not found"}
    )


@app.get("/api/sensors")
def get_all_sensors():
    return latest_data