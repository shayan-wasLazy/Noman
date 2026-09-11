# ⛏️ NOMAN

<p align="center">
  <strong>Intelligent Mine Monitoring & Early Warning System</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Smart%20India%20Hackathon-2026-blueviolet?style=for-the-badge">
  <img src="https://img.shields.io/badge/ESP32-IoT-black?style=for-the-badge&logo=espressif">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/PlatformIO-Embedded-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Chart.js-Visualization-FF6384?style=for-the-badge">
</p>

<p align="center">
  <i>Distributed sensing. Real-time intelligence. Safer mines.</i>
</p>

---

# 🧠 What is NOMAN?

**NOMAN** is a distributed IoT-based mine monitoring and early-warning system designed to continuously monitor acceleration and movement across different locations in a mining environment.

The system uses multiple **ESP32 sensor nodes** equipped with **ADXL345 accelerometers**.

Each node independently:

1. Measures acceleration along the X, Y and Z axes.
2. Connects to a Wi-Fi network.
3. Sends sensor readings to a central server.
4. Identifies itself using a unique `NODE_ID`.

A **FastAPI backend** receives the measurements, maintains the latest reading from every node, stores a rolling sensor history, and provides REST APIs to the monitoring dashboard.

The dashboard provides a centralized view of the entire sensor network.

---

# 🎯 Why NOMAN?

Mining environments can experience:

- Ground movement
- Structural instability
- Rock displacement
- Vibrations
- Subsidence
- Sudden changes in environmental conditions

Continuous monitoring can help identify unusual movement patterns before they become critical.

NOMAN is designed as a **low-cost and scalable prototype** that can place sensor nodes at multiple locations and bring their data into a single monitoring interface.

The current system focuses on:

> **Sense → Transmit → Process → Visualize**

Future versions can extend this into:

> **Sense → Transmit → Process → Detect → Predict → Warn**

---

# 🏗️ System Architecture

NOMAN follows a distributed architecture where multiple ESP32 sensor nodes transmit data wirelessly to a centralized FastAPI server.

```text
                     ┌─────────────────────┐
                     │     ADXL345 #1      │
                     └──────────┬──────────┘
                                │
                         ┌──────▼──────┐
                         │   ESP32 #1  │
                         │   NODE_01   │
                         └──────┬──────┘
                                │
                                │ Wi-Fi
                                │
                                │
                     ┌──────────▼──────────┐
                     │                     │
                     │    SERVER LAPTOP    │
                     │                     │
                     │       FastAPI       │
                     │       Backend       │
                     │                     │
                     └──────────┬──────────┘
                                │
                                │ HTTP / REST API
                                │
                         ┌──────▼──────┐
                         │    NOMAN    │
                         │  Dashboard  │
                         └─────────────┘
                                ▲
                                │
                                │ Wi-Fi
                                │
                    ┌───────────┴───────────┐
                    │                       │
             ┌──────▼──────┐         ┌──────▼──────┐
             │   ESP32 #2  │         │   ESP32 #3  │
             │   NODE_02   │         │   NODE_03   │
             └──────┬──────┘         └──────┬──────┘
                    │                       │
             ┌──────▼──────┐         ┌──────▼──────┐
             │  ADXL345 #2 │         │  ADXL345 #3 │
             └─────────────┘         └─────────────┘
```

## Runtime Data Flow

```text
ADXL345
   ↓
ESP32 Sensor Node
   ↓
Wi-Fi
   ↓
FastAPI Backend
   ↓
REST API
   ↓
NOMAN Dashboard
```

The laptop connected to an ESP32 for programming is **not required to be part of the runtime data path**.

---

# 🧩 Core Components

| Component | Purpose |
|---|---|
| ESP32 | Wireless sensor node |
| ADXL345 | 3-axis acceleration measurement |
| Wi-Fi | Wireless communication |
| FastAPI | Backend API and data processing |
| Python | Backend runtime |
| Chart.js | Data visualization |
| PlatformIO | ESP32 development and firmware management |
| VS Code | Development environment |

---

# 🔌 Hardware Setup

## ADXL345 → ESP32

The ADXL345 communicates with the ESP32 using I²C.

| ADXL345 | ESP32 |
|---|---|
| VCC | 3.3V |
| GND | GND |
| SDA | GPIO 21 |
| SCL | GPIO 22 |

> **Important:** Use 3.3V for the ADXL345 unless your particular breakout board explicitly supports 5V input.

---

# 📁 Project Structure

```text
Noman/
│
├── backend/
│   ├── frontend/
│   │   └── index.html
│   └── main.py
│
├── include/
│   └── env_config.h
│
├── lib/
│
├── scripts/
│   └── load_env.py
│
├── src/
│   └── main.cpp
│
├── test/
│
├── .env
├── .env_sample.txt
├── .gitignore
├── platformio.ini
├── readme.md
└── requirements.txt
```

> `include/env_config.h` is generated automatically during the PlatformIO build from the local `.env` file.

---

# ⚙️ Backend Setup

The NOMAN backend is built using **FastAPI**.

## Create the Backend Environment

Create a Python virtual environment in the project root.

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Start the FastAPI Server

From the project root, move into the backend directory.

### Windows

```powershell
cd backend
..\venv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### macOS / Linux

```bash
cd backend
source ../venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The dashboard will be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

# 📡 ESP32 Node Setup

NOMAN uses the **same PlatformIO project and firmware for every ESP32 sensor node**.

Each physical ESP32 is assigned a unique `NODE_ID`.

Example:

```text
NODE_01
NODE_02
NODE_03
```

The node-specific configuration is stored in the local `.env` file.

---

# 💻 Setting Up NODE_02 on Another Laptop

NOMAN supports programming sensor nodes from different laptops.

The laptop connected to **NODE_02 does not need to run the backend**.

It is only used for:

- Cloning the repository
- Configuring the node
- Building the firmware
- Uploading the firmware
- Monitoring the ESP32

The ESP32 communicates directly with the laptop running the FastAPI server over Wi-Fi.

```text
                 Wi-Fi Network
                      │
          ┌───────────┴───────────┐
          │                       │
     ESP32 NODE_01          ESP32 NODE_02
          │                       │
          │                       │
          └───────────┬───────────┘
                      │
                      ▼
               SERVER LAPTOP
              ┌─────────────┐
              │   FastAPI   │
              │   Backend   │
              │  Dashboard  │
              └─────────────┘

NODE_02 Laptop
      │
      └── USB ──► NODE_02

The NODE_02 laptop is only used for development,
firmware upload and serial monitoring.
```

---

## 1. Clone the Repository

On the laptop that will be used to program NODE_02:

### Windows

```powershell
git clone https://github.com/shayan-wasLazy/Noman.git
cd Noman
```

### macOS

```bash
git clone https://github.com/shayan-wasLazy/Noman.git
cd Noman
```

Open the cloned project in VS Code:

```bash
code .
```

If the `code` command is not available, open VS Code manually and select the cloned `Noman` folder.

---

## 2. Install PlatformIO

Install the following on the NODE_02 laptop:

- **Visual Studio Code**
- **PlatformIO IDE extension**

PlatformIO is used to:

- Build the ESP32 firmware
- Install required libraries
- Upload firmware
- Monitor the ESP32

The Arduino IDE is not required.

---

## 3. Connect NODE_02

Connect the NODE_02 ESP32 to the laptop using a USB data cable.

### Windows

Check the ESP32's COM port from:

```text
Device Manager
→ Ports (COM & LPT)
```

Example:

```text
COM3
COM5
COM9
```

### macOS

Open Terminal and run:

```bash
ls /dev/cu.*
```

Example:

```text
/dev/cu.usbserial-0001
```

The port may be different on every computer.

---

## 4. Create the Node Configuration

The repository contains an example configuration file:

```text
.env_sample.txt
```

Create a local `.env` file from it.

### Windows

```powershell
Copy-Item .env_sample.txt .env
```

### macOS

```bash
cp .env_sample.txt .env
```

Open `.env` and configure NODE_02:

```env
WIFI_SSID=YOUR_WIFI_NAME
WIFI_PASSWORD=YOUR_WIFI_PASSWORD

BACKEND_HOST=SERVER_LAPTOP_IP
BACKEND_PORT=8000

NODE_ID=NODE_02
```

For example:

```env
WIFI_SSID=YOUR_WIFI_NAME
WIFI_PASSWORD=YOUR_WIFI_PASSWORD

BACKEND_HOST=10.155.71.195
BACKEND_PORT=8000

NODE_ID=NODE_02
```

---

## 5. Configure the Backend Address

`BACKEND_HOST` must contain the **IP address of the laptop running the NOMAN FastAPI backend**.

For example:

```text
                    Wi-Fi Network
                         │
                         │
              ┌──────────▼──────────┐
              │    SERVER LAPTOP    │
              │                     │
              │      FastAPI        │
              │      :8000          │
              │                     │
              │  10.155.71.195      │
              └──────────┬──────────┘
                         ▲
                         │
                         │ Wi-Fi
                         │
                  ┌──────┴──────┐
                  │   ESP32     │
                  │   NODE_02   │
                  └──────┬──────┘
                         │
                      ADXL345
```

Therefore:

```env
BACKEND_HOST=10.155.71.195
BACKEND_PORT=8000
```

### Important

Do **not** set:

```env
BACKEND_HOST=localhost
```

or:

```env
BACKEND_HOST=127.0.0.1
```

The ESP32 must connect to the **server laptop's network IP**, not the laptop being used to program NODE_02.

---

## 6. Set the NODE_ID

Every ESP32 must have a unique `NODE_ID`.

For NODE_02:

```env
NODE_ID=NODE_02
```

For example, a larger deployment could use:

```text
NODE_01
NODE_02
NODE_03
NODE_04
NODE_05
```

All nodes can use the **same NOMAN repository and firmware**.

Only the local `.env` configuration needs to change.

```text
                 NOMAN Repository
                        │
          ┌─────────────┼─────────────┐
          │             │             │
          ▼             ▼             ▼
       NODE_01       NODE_02       NODE_03
          │             │             │
          ▼             ▼             ▼
     NODE_ID=01    NODE_ID=02    NODE_ID=03
```

---

## 7. Build the Firmware

From the root of the cloned NOMAN project, run:

```bash
pio run
```

During the build, NOMAN's environment script:

```text
scripts/load_env.py
```

reads the local `.env` configuration and generates:

```text
include/env_config.h
```

The generated configuration is then compiled into the ESP32 firmware.

`env_config.h` does not need to be manually created or edited.

---

## 8. Upload the Firmware

With NODE_02 connected to the laptop:

```bash
pio run --target upload
```

PlatformIO will compile the firmware and upload it to the ESP32.

If PlatformIO does not automatically detect the ESP32, specify the port manually.

### Windows

```bash
pio run --target upload --upload-port COM9
```

Replace `COM9` with the actual COM port shown on that laptop.

### macOS

```bash
pio run --target upload --upload-port /dev/cu.usbserial-0001
```

Replace the port with the actual device shown by:

```bash
ls /dev/cu.*
```

---

## 9. Monitor NODE_02

Open the ESP32 serial monitor:

```bash
pio device monitor --baud 115200
```

The ESP32 should display:

```text
================================
SIH26025 MINE MONITORING NODE
================================

Node ID: NODE_02

Connecting to WiFi...

WiFi connected!

IP Address: 10.155.71.82

Backend:
http://10.155.71.195:8000/api/sensor

Initializing ADXL345...

ADXL345 initialized

================================
```

Sensor readings should then appear:

```text
Sensor reading:

X: 0.508
Y: 0.884
Z: 0.308

Sending sensor data...

{"node_id":"NODE_02","x":0.508,"y":0.884,"z":0.308}

HTTP Response: 200
```

An HTTP response of:

```text
200
```

indicates that the FastAPI backend successfully received the sensor data.

---

# 🌐 Multi-Laptop Deployment

NOMAN does not require every ESP32 to be connected to the same laptop.

A possible deployment is:

```text
                         Wi-Fi Network
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
          NODE_01         NODE_02         NODE_03
           ESP32           ESP32           ESP32
              │               │               │
              │ USB           │ USB           │ USB
              ▼               ▼               ▼
          Laptop A         Laptop B         Laptop C
         Development      Development      Development


                     ┌─────────────────┐
                     │  SERVER LAPTOP  │
                     │                 │
                     │    FastAPI      │
                     │    Backend      │
                     │                 │
                     │    Dashboard    │
                     └─────────────────┘
```

The development laptops are only required when programming or monitoring the ESP32 nodes.

Once programmed, each ESP32 communicates directly with the server over Wi-Fi.

---

# 🔄 NODE_02 Setup Flow

After cloning the repository onto another laptop:

```text
Clone Repository
       ↓
Open in VS Code
       ↓
Install PlatformIO
       ↓
Connect NODE_02
       ↓
Create local .env
       ↓
Set NODE_ID=NODE_02
       ↓
Set BACKEND_HOST=SERVER_IP
       ↓
Build Firmware
       ↓
Upload to ESP32
       ↓
Open Serial Monitor
       ↓
ESP32 connects to Wi-Fi
       ↓
ESP32 sends sensor data
       ↓
FastAPI receives data
       ↓
NOMAN Dashboard displays NODE_02
```

---

# 🔐 Node Configuration & Security

The `.env` file is **local to each laptop** and should not be committed to the repository.

It contains configuration such as:

```text
Wi-Fi SSID
Wi-Fi Password
Backend IP
Backend Port
Node ID
```

Each node can therefore have its own configuration.

### NODE_01

```env
NODE_ID=NODE_01
BACKEND_HOST=SERVER_IP
```

### NODE_02

```env
NODE_ID=NODE_02
BACKEND_HOST=SERVER_IP
```

### NODE_03

```env
NODE_ID=NODE_03
BACKEND_HOST=SERVER_IP
```

The repository should contain:

```text
.env_sample.txt
```

but the actual:

```text
.env
```

should remain local.

Generated configuration files such as:

```text
include/env_config.h
```

should also remain local.

Recommended `.gitignore` entries:

```gitignore
.env
*.pyc
__pycache__/
.pio/
venv/
.vscode/
include/env_config.h
```

---

# 📡 Network Requirements

For NODE_02 to communicate with the backend:

```text
ESP32 NODE_02
      │
      │ Wi-Fi
      ▼
Network / Router / Hotspot
      │
      ▼
Server Laptop
      │
      │ Port 8000
      ▼
FastAPI Backend
      │
      ▼
NOMAN Dashboard
```

The ESP32 and server laptop must have network connectivity to each other.

The FastAPI server should listen on:

```text
0.0.0.0:8000
```

For example:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

# 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/sensor` | Receive sensor data |
| `GET` | `/api/sensors` | Get latest data from all nodes |
| `GET` | `/api/sensor/{node_id}` | Get latest data for a node |
| `GET` | `/api/sensor/{node_id}/history` | Get historical data for a node |
| `GET` | `/api/history` | Get sensor history |

FastAPI documentation:

```text
http://SERVER_IP:8000/docs
```

---

# 📊 Dashboard

The NOMAN dashboard provides a centralized monitoring interface.

It displays:

- Total connected nodes
- Online/offline node status
- Latest sensor readings
- X-axis acceleration
- Y-axis acceleration
- Z-axis acceleration
- Historical sensor data
- Real-time sensor charts

The dashboard communicates with the FastAPI backend using REST APIs.

---

# ⚠️ Troubleshooting

## ESP32 connects to Wi-Fi but `HTTP Response: -1`

This generally means that the ESP32 could not establish a connection with the backend.

Check:

1. FastAPI is running on the server laptop.
2. `BACKEND_HOST` contains the server laptop's IP address.
3. The ESP32 can reach the server laptop over the network.
4. FastAPI is listening on `0.0.0.0`.
5. Port `8000` is not blocked by the server's firewall.

---

## Wi-Fi connects but backend does not

Check the complete network path:

```text
ESP32
  │
  │ Wi-Fi
  ▼
Network
  │
  ▼
Server Laptop
  │
  └── Port 8000
          │
          ▼
       FastAPI
```

The ESP32 should use the **server laptop's IP address**.

---

## PlatformIO cannot find the ESP32

### Windows

Check:

```text
Device Manager → Ports (COM & LPT)
```

### macOS

Run:

```bash
ls /dev/cu.*
```

Also try:

- A different USB port
- A different USB cable
- A known data-capable USB cable

Some USB cables provide power but do not support data transfer.

---

## `env_config.h` is missing

Run:

```bash
pio run
```

The file is automatically generated by:

```text
scripts/load_env.py
```

Do not manually create it.

---

# 🚀 Adding More Sensor Nodes

To add another sensor node:

1. Connect a new ESP32 to any development laptop.
2. Clone the NOMAN repository.
3. Create a local `.env`.
4. Set a unique `NODE_ID`.
5. Set `BACKEND_HOST` to the server laptop's IP.
6. Build and upload the same firmware.

For example:

```text
NODE_01 ─┐
NODE_02 ─┤
NODE_03 ─┤
NODE_04 ─┤─── Wi-Fi ───► FastAPI ───► Dashboard
NODE_05 ─┤
NODE_06 ─┘
```

This allows NOMAN to scale from a small prototype to a distributed network of sensor nodes.

---

# 🔮 Future Scope

Potential future improvements include:

- Vibration anomaly detection
- Machine-learning based anomaly classification
- Ground movement prediction
- Threshold-based early warnings
- SMS / email / notification alerts
- Sensor fusion
- Additional environmental sensors
- GPS-based node positioning
- Long-range communication using LoRa
- Persistent database storage
- Automated incident logging
- Edge-based anomaly detection
- Historical trend analysis
- Risk scoring for individual mining zones

The long-term objective is to evolve NOMAN from a monitoring platform into a complete intelligent early-warning system:

> **Sense → Transmit → Process → Detect → Predict → Warn**

---

# 🛠️ Development Workflow

```text
Developer
   │
   ▼
VS Code + PlatformIO
   │
   ▼
ESP32 Firmware
   │
   ▼
ADXL345 Sensor
   │
   ▼
Wi-Fi
   │
   ▼
FastAPI Backend
   │
   ├── Latest Sensor Data
   ├── Historical Data
   └── REST API
   │
   ▼
NOMAN Dashboard
```

---

# 📌 Key Design Principles

### Distributed

Multiple sensor nodes can operate at different physical locations.

### Scalable

New ESP32 nodes can be added without creating separate PlatformIO projects.

### Low Cost

The prototype uses affordable and widely available hardware.

### Network-Based

Sensor nodes communicate wirelessly with a centralized server.

### Platform Independent

The same repository can be used to program nodes from Windows or macOS.

### Modular

Hardware, firmware, backend and visualization are separated into distinct components.

---

# ⛏️ NOMAN

<p align="center">
  <strong>Intelligent Mine Monitoring & Early Warning System</strong>
</p>

<p align="center">
  <i>Distributed sensing. Real-time intelligence. Safer mines.</i>
</p>

<p align="center">
  <strong>Know the ground before it moves.</strong>
</p>
