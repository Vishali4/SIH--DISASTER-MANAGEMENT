# 09 Power System Architecture

To operate in remote disaster-prone zones, both sensor nodes must remain fully off-grid using solar power.

## 1. Node Power Consumption Diagram

```text
  Solar Panel (12V, 10W)
           |
           v
Solar Charge Controller (12V, 10A) <---> Rechargeable Battery (LiFePO4, 12V 6Ah)
           |
           v
   Buck Converter (Step-down to 5V / 3.3V)
           |
    +------+------+
    v             v
  ESP32      LoRa Module & Sensors
```

## 2. Component Specifications

### A. Solar Panel
- **Rating**: 10 Watts, 12 Volt monocrystalline.
- **Purpose**: Generates charge during daylight hours.

### B. Solar Charge Controller
- **Rating**: 10A PWM controller.
- **Features**: Prevents battery overcharging, over-discharging, and protects against reverse current leakage during night hours.

### C. Battery Pack
- **Chemistry**: Lithium Iron Phosphate (LiFePO4) or Sealed Lead Acid (SLA).
- **Capacity**: 12V, 6Ah. Offers high thermal stability and longer life cycle compared to standard Li-Po batteries.

### D. Buck Converter
- **Component**: LM2596 step-down regulator.
- **Input**: 12V from charge controller output.
- **Output**: Adjusted to 5.0V (for powering the ESP32 via VIN pin and MQ-2/ultrasonic sensor lines) and 3.3V (for DHT11/LoRa).

## 3. Power Saving Logic
To extend battery runtime during cloudy seasons, ESP32 nodes utilize sleep features:
- Put the LoRa radio into Sleep Mode.
- Enter ESP32 Deep Sleep for 5 seconds between measurements.
- Wake up via Timer interrupt, compile sensor measurements, transmit, and loop back to deep sleep.
