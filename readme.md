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

NOMAN follows a distributed architecture.

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
                     │      FastAPI        │
                     │      Backend        │
                     │                     │
                     └──────────┬──────────┘
                                │
                                │ HTTP / REST API
                                │
                         ┌──────▼──────┐
                         │   NOMAN     │
                         │  Dashboard  │
                         └─────────────┘
                                ▲
                                │
                                │ Wi-Fi
                                │
                     ┌──────────┴──────────┐
                     │                     │
              ┌──────┴──────┐       ┌─────┴───────┐
              │   ESP32 #2  │       │   ESP32 #3  │
              │   NODE_02   │       │   NODE_03   │
              └──────┬──────┘       └─────┬───────┘
                     │                     │
              ┌──────▼──────┐       ┌─────▼───────┐
              │  ADXL345 #2 │       │  ADXL345 #3 │
              └─────────────┘       └─────────────┘