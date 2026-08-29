# Environmental Intelligence Network - User Stories

This document outlines the user stories, use cases, and acceptance criteria for the Environmental Intelligence Network prototype, mapped to various stakeholders (Disaster Management Officials, Edge Hub Operators, Field Engineers, and Local Residents).

---

## 👥 Stakeholder Personas
1. **Local Resident (Remote Area)**: Needs fast, reliable warnings to evacuate or secure property during sudden floods or forest fires.
2. **Disaster Management Operator (Pi Hub Station)**: Needs real-time, high-confidence alerts, live charts, and sensor telemetry from local nodes to assess environmental risks.
3. **Field Deployment Engineer**: Needs to quickly set up, monitor, and diagnose ESP32 sensor nodes and RPi hubs in off-grid solar environments.

---

## 📋 User Stories

### Story 1: Local Warning Alerts (Local Resident)
> **As a** remote area resident,  
> **I want** a clear visual and audible alarm directly at the central hub location,  
> **So that** I am immediately notified of critical environmental hazards (rising flood waters or nearby forest fires) even if the internet or cellular network is completely down.

#### Acceptance Criteria:
- [ ] **Audible Indicator**: Under `NORMAL` conditions, the buzzer must remain off. Under `WARNING` conditions, the buzzer sounds intermittently. Under `CRITICAL` conditions, the buzzer sounds continuously.
- [ ] **Visual Indicator**: The hub's status LEDs change colors dynamically: Green for `NORMAL`, Yellow for `WARNING`, and Red for `HIGH`/`CRITICAL`.
- [ ] **LCD Screen**: A 16x2 I2C LCD screen must update locally to show the real-time status of both nodes (e.g., `FL:NORMAL FR:CRITICAL`) and the aggregated alert level.

---

### Story 2: Edge-AI Offline Risk Assessment (Disaster Management Operator)
> **As a** disaster management operator,  
> **I want** the central hub to automatically analyze multiple raw sensor feeds using an offline Machine Learning model,  
> **So that** it accurately identifies hazard conditions, minimizes false alarms, and provides a clear risk level with a confidence score without requiring cloud resources.

#### Acceptance Criteria:
- [ ] **Model Execution**: The hub loads pre-trained decision-tree classifiers (`flood_model.joblib` and `fire_model.joblib`) locally.
- [ ] **Data Validation**: System validates incoming LoRa packets, discarding corrupted packages before passing them to the Edge-AI engine.
- [ ] **Confidence Metric**: Every classification outputs one of four risk levels (`NORMAL`, `WARNING`, `HIGH`, `CRITICAL`) along with a confidence percentage (0% to 100%).
- [ ] **Resilient Heuristics**: If the machine learning model fails to load, the system falls back onto predefined rule-based heuristics to guarantee uninterrupted safety monitoring.

---

### Story 3: Real-Time Offline Web Dashboard (Operator / Field Engineer)
> **As a** field operator at a remote base station,  
> **I want** to access a visual web dashboard hosted locally on the Raspberry Pi,  
> **So that** I can view real-time sensor graphs, historical trends, and system status charts using my phone or laptop over a local hotspot.

#### Acceptance Criteria:
- [ ] **No Internet Dependency**: All dashboard assets (CSS, JS, Fonts) must function completely offline.
- [ ] **Live Polling**: The frontend dashboard polls the local Flask REST API (`/api/status`) every 2 seconds to update sensor readings and log lists.
- [ ] **Sensor Trend Graphs**: Shows chronological trends of water level distance and smoke density using Chart.js.
- [ ] **Responsive Design**: The dashboard utilizes a premium glassmorphic dark theme that fits perfectly on smartphones, tablets, and desktop displays.

---

### Story 4: Off-Grid Hardware Diagnostics (Field Deployment Engineer)
> **As a** field deployment engineer,  
> **I want** the ESP32 sensor nodes to send telemetry packet statistics (packet IDs, node IDs) over LoRa,  
> **So that** I can easily test the transmission range, track packet loss, and verify solar battery state in off-grid locations.

#### Acceptance Criteria:
- [ ] **Unique Node Identifiers**: Flood node must send packets with `nodeId = 1`, and Fire node must use `nodeId = 2`.
- [ ] **Sequence Tracking**: Each packet includes an incrementing `packetId` sequence counter to detect gaps or packet losses.
- [ ] **Persistent Log File**: All incoming packets and assessments are logged permanently to a local SQLite database (`disaster_data.db`) on the Raspberry Pi for offline review.
