from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict
import os

from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException

from fastapi.staticfiles import StaticFiles

from fastapi.responses import FileResponse


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(
    BASE_DIR / ".env"
)


APP_HOST = os.getenv(
    "APP_HOST",
    "0.0.0.0"
)

APP_PORT = int(
    os.getenv(
        "APP_PORT",
        "8000"
    )
)

NODE_TIMEOUT_SECONDS = int(
    os.getenv(
        "NODE_TIMEOUT_SECONDS",
        "5"
    )
)

MAX_HISTORY = int(
    os.getenv(
        "MAX_HISTORY",
        "300"
    )
)


# ============================================================
# FASTAPI
# ============================================================

app = FastAPI(
    title="SIH26025 Mine Monitoring API"
)


# ============================================================
# FRONTEND
# ============================================================

FRONTEND_DIR = (
    BASE_DIR / "frontend"
)


app.mount(
    "/static",
    StaticFiles(
        directory=FRONTEND_DIR
    ),
    name="static"
)


@app.get("/")
def frontend():

    return FileResponse(
        FRONTEND_DIR /
        "index.html"
    )


# ============================================================
# SENSOR STORAGE
# ============================================================

latest_data = {}

sensor_history = defaultdict(
    list
)


# ============================================================
# RECEIVE SENSOR DATA
# ============================================================

@app.post("/api/sensor")
def receive_sensor_data(
    data: dict
):

    node_id = data.get(
        "node_id"
    )


    if not node_id:

        raise HTTPException(
            status_code=400,
            detail="node_id is required"
        )


    try:

        x = float(
            data.get(
                "x"
            )
        )

        y = float(
            data.get(
                "y"
            )
        )

        z = float(
            data.get(
                "z"
            )
        )

    except (
        TypeError,
        ValueError
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid sensor values"
        )


    # --------------------------------------------------------
    # Timestamp
    # --------------------------------------------------------

    timestamp = datetime.now(
        timezone.utc
    ).isoformat()


    # --------------------------------------------------------
    # Normalized reading
    # --------------------------------------------------------

    reading = {

        "node_id":
            node_id,

        "x":
            x,

        "y":
            y,

        "z":
            z,

        "timestamp":
            timestamp

    }


    # --------------------------------------------------------
    # Latest
    # --------------------------------------------------------

    latest_data[
        node_id
    ] = reading


    # --------------------------------------------------------
    # History
    # --------------------------------------------------------

    sensor_history[
        node_id
    ].append(
        reading
    )


    # --------------------------------------------------------
    # Limit history
    # --------------------------------------------------------

    if len(
        sensor_history[node_id]
    ) > MAX_HISTORY:

        sensor_history[node_id] = (
            sensor_history[node_id]
            [-MAX_HISTORY:]
        )


    # --------------------------------------------------------
    # Terminal output
    # --------------------------------------------------------

    print(
        "\n========== SENSOR DATA =========="
    )

    print(
        f"NODE : {node_id}"
    )

    print(
        f"X    : {x:.4f} g"
    )

    print(
        f"Y    : {y:.4f} g"
    )

    print(
        f"Z    : {z:.4f} g"
    )

    print(
        f"TIME : {timestamp}"
    )


    return {

        "status":
            "success",

        "node_id":
            node_id,

        "timestamp":
            timestamp

    }


# ============================================================
# ALL LATEST SENSOR DATA
# ============================================================

@app.get("/api/sensors")
def get_all_sensors():

    return latest_data


# ============================================================
# SINGLE NODE
# ============================================================

@app.get(
    "/api/sensor/{node_id}"
)
def get_sensor_data(
    node_id: str
):

    if node_id not in latest_data:

        raise HTTPException(
            status_code=404,
            detail="Node not found"
        )


    return latest_data[
        node_id
    ]


# ============================================================
# NODE HISTORY
# ============================================================

@app.get(
    "/api/sensor/{node_id}/history"
)
def get_sensor_history(
    node_id: str
):

    return {

        "node_id":
            node_id,

        "history":
            sensor_history.get(
                node_id,
                []
            )

    }


# ============================================================
# ALL HISTORY
# ============================================================

@app.get(
    "/api/history"
)
def get_all_history():

    return sensor_history