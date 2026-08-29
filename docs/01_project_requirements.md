# 01 Project Requirements

## 1. Goal
Develop a distributed, low-power Environmental Intelligence Network capable of detecting environmental hazards (floods, forest fires) early, processing critical information locally, and providing immediate warnings without depending on continuous Internet or cloud connectivity.

## 2. Functional Requirements
- **Local Detection**: Continuous monitoring of flood indicators (water level, rain) and forest-fire indicators (smoke, flame) at sensor nodes.
- **Offline Mesh/Point-to-Point Transmission**: Low-power, long-range wireless data communication between sensor nodes and central hub.
- **Edge AI Inference**: Local risk assessment of environment metrics using machine learning models deployed directly on a Raspberry Pi.
- **Warning System**: Real-time updates via localized LCD screen, multicolor status LEDs, and audible buzzers depending on risk severity.
- **Off-Grid Operation**: Powered completely by solar panels, batteries, and charge controllers.

## 3. Non-Functional Requirements
- **Zero Cloud/Internet Dependency**: Critical warning pipelines must work 100% offline.
- **Low Power Consumption**: ESP32 transmitter nodes must utilize low-power sleep modes to conserve battery.
- **Range**: Secure a connection range of at least 1–5 km using LoRa technology under line-of-sight.
- **Data Integrity**: Filter invalid or corrupted packets at the receiver node.
