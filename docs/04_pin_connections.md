# 04 Pin Connections

## 1. ESP32 Node 1: Flood Monitoring

### Sensors
- **DHT11 (Temp/Hum)**:
  - VCC -> ESP32 3.3V
  - GND -> ESP32 GND
  - DATA -> ESP32 GPIO 4
- **Ultrasonic (HC-SR04)**:
  - VCC -> ESP32 5V (VIN)
  - GND -> ESP32 GND
  - TRIG -> ESP32 GPIO 12
  - ECHO -> ESP32 GPIO 13 (requires level shifter or voltage divider if using 5V echo to 3.3V pin)
- **Rain Sensor**:
  - VCC -> ESP32 3.3V
  - GND -> ESP32 GND
  - AO (Analog Out) -> ESP32 GPIO 34 (ADC1_CH6)

### LoRa Module (SX1278 SPI)
- VCC -> ESP32 3.3V
- GND -> ESP32 GND
- NSS (CS) -> ESP32 GPIO 5
- RST -> ESP32 GPIO 14
- DIO0 -> ESP32 GPIO 2
- SCK -> ESP32 GPIO 18
- MISO -> ESP32 GPIO 19
- MOSI -> ESP32 GPIO 23

---

## 2. ESP32 Node 2: Forest-Fire Monitoring

### Sensors
- **DHT11 (Temp/Hum)**:
  - VCC -> ESP32 3.3V
  - GND -> ESP32 GND
  - DATA -> ESP32 GPIO 4
- **MQ-2 (Smoke/Gas)**:
  - VCC -> ESP32 5V (VIN)
  - GND -> ESP32 GND
  - AO (Analog Out) -> ESP32 GPIO 34
- **Flame Sensor**:
  - VCC -> ESP32 3.3V
  - GND -> ESP32 GND
  - DO (Digital Out) -> ESP32 GPIO 35 (Input Only pin)

### LoRa Module (SX1278 SPI)
- Same connection configuration as Node 1.

---

## 3. Raspberry Pi 4 Model B (Alert Hub)

### I2C LCD Display (16x2)
- VCC -> Pi 5V (Pin 2 or 4)
- GND -> Pi GND (Pin 6 or 9)
- SDA -> Pi GPIO 2 (Pin 3 / SDA)
- SCL -> Pi GPIO 3 (Pin 5 / SCL)

### Alert LEDs & Buzzers
- **Green LED**: Positive -> Pi GPIO 17 (Pin 11) + 220 ohm resistor -> GND
- **Yellow LED**: Positive -> Pi GPIO 27 (Pin 13) + 220 ohm resistor -> GND
- **Red LED**: Positive -> Pi GPIO 22 (Pin 15) + 220 ohm resistor -> GND
- **Buzzer**: Positive -> Pi GPIO 18 (Pin 12 / PWM) -> GND
