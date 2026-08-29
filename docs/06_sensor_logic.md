# 06 Sensor Logic

## 1. Flood Monitoring Node (Node 1)

### A. Water Level Distance
Uses the **HC-SR04** ultrasonic sensor.
- The sensor outputs an ultrasound burst.
- It measures echo duration in microseconds.
- Formula to calculate distance in centimeters:
  $$\text{Distance (cm)} = \frac{\text{Echo Pulse Time in Microseconds} \times 0.0343}{2}$$
- **Threshold logic**: A shorter distance means the water surface is getting closer to the sensor, indicating rising flood level.

### B. Rainfall Intensity
Uses an analog rain sensor.
- High analog values (near 4095) represent dry conditions.
- Low values (near 0) represent heavy rain saturating the sensor plate.

---

## 2. Forest-Fire Monitoring Node (Node 2)

### A. Smoke & Carbon Monoxide Level
Uses the **MQ-2** gas/smoke sensor.
- Requires preheating for stable readings.
- Measures smoke density by reading the analog voltage output.
- Higher analog values indicate elevated concentrations of smoke/combustion products.

### B. Flame Presence
Uses an **Infrared Flame Sensor**.
- Detects light waves with wavelengths between 760nm to 1100nm emitted by flames.
- High sensitivity range.
- Output signal is active low (returns `LOW` or `0` on flame presence, `HIGH` or `1` during normal state).
- The node code flips this logic to pack `1` on detection and `0` for normal.
