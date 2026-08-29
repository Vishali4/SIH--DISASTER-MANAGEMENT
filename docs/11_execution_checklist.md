# 11 Execution Checklist

Use this checklist during field deployment to track system assembly and launch.

## 🟩 Phase 1: Pre-Deployment Build
- [x] Write ESP32 flood node C++ code.
- [x] Write ESP32 fire node C++ code.
- [x] Implement Raspberry Pi central parser (`main.py`).
- [x] Train ML models (`train_model.py`) and save `.joblib` objects.
- [x] Build web interface status dashboard.

## 🟨 Phase 2: Hardware Assembly & Bench Testing
- [ ] Connect DHT11, Rain, and Ultrasonic sensors to ESP32 Node 1 on breadboard.
- [ ] Connect DHT11, MQ-2, and Flame sensors to ESP32 Node 2.
- [ ] Connect SX1278 SPI LoRa modules to both ESP32 units.
- [ ] Connect SX1278 transceiver and I2C LCD display to Raspberry Pi GPIOs.
- [ ] Upload sketches and confirm serial feeds show valid telemetry.
- [ ] Power on Raspberry Pi and launch `main.py` with actual receiver module.

## 🟧 Phase 3: Power Integration & Waterproofing
- [ ] Calibrate LM2596 buck converters to output exactly 5.0V.
- [ ] Connect Solar Panel -> Charge Controller -> Battery -> Buck Converter -> Nodes.
- [ ] Seal ESP32 nodes inside IP65 waterproof enclosures.
- [ ] Mount waterproof ultrasonic sensor pointing downward inside pipe/bucket bracket.
- [ ] Secure MQ-2 and flame sensors inside shielded, ventilated housings.

## 🟥 Phase 4: Full Deployment & Field Launch
- [ ] Deploy Node 1 near water body / stream simulation.
- [ ] Deploy Node 2 in elevated forest mock zone.
- [ ] Boot Raspberry Pi Alert Hub at base station.
- [ ] Verify that live logs appear on the local offline dashboard (`http://localhost:5000`).
- [ ] Confirm alert LED and buzzers operate correctly during simulated fire/flood states.
