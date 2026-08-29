# 05 LoRa Protocol Specification

To communicate offline, the sensor nodes and alert hub utilize structured binary packets over standard LoRa physical layer frequency modulation.

## 1. Physical Layer Configuration
- **Frequency**: 433.0 MHz (or 868.0 MHz / 915.0 MHz depending on regional regulatory approval)
- **Spreading Factor (SF)**: 7 (provides optimized balance between range and transmission speed)
- **Coding Rate (CR)**: 4/5 (adds error correction bytes to counter packet corruption)
- **Bandwidth**: 125 kHz
- **TX Power**: 17 dBm (configurable up to 20 dBm)

## 2. Frame Structure
Payloads are transmitted as binary structs to reduce air-time, saving battery.

### Packet Struct Format: Node 1 (Flood)
Total packet size: 21 bytes.
- **Node ID** (1 byte): `0x01`
- **Packet ID** (4 bytes): Sequential integer counter (unsigned long)
- **Temperature** (4 bytes): IEEE 754 float
- **Humidity** (4 bytes): IEEE 754 float
- **Water Distance** (4 bytes): Float value in centimeters
- **Rain Value** (4 bytes): Analog value (integer range: 0 to 4095)

### Packet Struct Format: Node 2 (Forest Fire)
Total packet size: 21 bytes.
- **Node ID** (1 byte): `0x02`
- **Packet ID** (4 bytes): Sequential integer counter (unsigned long)
- **Temperature** (4 bytes): IEEE 754 float
- **Humidity** (4 bytes): IEEE 754 float
- **Smoke Value** (4 bytes): Analog value (integer range: 0 to 4095)
- **Flame Detected** (4 bytes): Integer boolean flag (1 = detected, 0 = normal)

## 3. Communication Strategy
- **Transmission Mode**: simplex/unidirectional periodic beaconing.
- **Interval**: Nodes transmit sensor packets every 5 seconds.
- **Collisions**: Standard randomized delay offset (+/- 250ms) is applied between cycles to avoid packet collision between nodes.
