# 10 System Testing Plan

## 1. Simulation Testing

### A. AI Classification Models
Validate predictions with boundary input ranges.
- Run `python raspberry_pi/edge_ai.py` to confirm that edge AI executes successfully and returns classification values without exception.

### B. Hub Orchestration (Dry Run)
Check the hub workflow with simulated packets.
- Launch `python raspberry_pi/main.py`. Ensure that incoming simulated packets from Node 1 and Node 2 are logged to database, assessed correctly, and outputted onto the console dashboard.

---

## 2. Hardware Testing

### A. Sensor Verification
Test sensor ranges and readings via Serial Monitor.
- Upload `flood_node.ino` to ESP32 #1 and check sensor print logs on Arduino Serial Monitor (115200 baud).
- Verify ultrasonic sensor readings change relative to bucket water levels.
- Upload `fire_node.ino` to ESP32 #2. Verify MQ-2 and Flame sensor states by introducing controlled smoke.

### B. Range & LoRa Link Testing
Evaluate LoRa signal quality.
- Deploy the ESP32 transmitter node and move away from the RPi hub.
- Measure packet loss rate (Packet sequence count tracking on Hub).
- Analyze RSSI (Received Signal Strength Indicator) and SNR (Signal-to-Noise Ratio) to find maximum functional communication range.
