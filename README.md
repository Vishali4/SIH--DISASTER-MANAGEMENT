# SIH - Environmental Intelligence Early-Warning Network

A distributed, offline-capable Environmental Intelligence Network prototype for detecting flood and forest fire hazards early, processing data locally, and displaying alerts using Edge AI on Raspberry Pi.

## 🚀 System Architecture

- **ESP32 Node 1 (Flood Node)**: Uses ultrasonic (water level), rain, and DHT11 sensors. Communicates status via LoRa.
- **ESP32 Node 2 (Fire Node)**: Uses MQ-2 smoke sensor, flame sensor, and DHT11. Communicates status via LoRa.
- **Raspberry Pi Central Hub**: Receives sensor data packets, validates them, performs local Edge AI risk assessment (using pre-trained models), triggers hardware warnings (LEDs + Buzzers + 16x2 I2C LCD), logs data to SQLite database, and runs a local Web Dashboard for offline analytics.

---

## 📂 Project Structure

```text
SIH-DISASTER-MANAGEMENT/
├── requirements.txt         # Python dependencies
├── README.md                # System setup & architecture documentation
├── esp32/
│   ├── flood_node/
│   │   └── flood_node.ino   # ESP32 Flood Node source code
│   └── fire_node/
│       └── fire_node.ino    # ESP32 Fire Node source code
└── raspberry_pi/
    ├── main.py              # Central orchestrator & serial LoRa parser
    ├── edge_ai.py           # Local inference engine & hazard classifier
    ├── train_model.py       # ML training script to generate risk models
    ├── database.py          # SQLite database logging interface
    ├── hardware_control.py  # GPIO controller for LEDs, buzzer, and I2C LCD
    └── dashboard/           # Local visualization server
        ├── app.py           # Flask backend application
        └── templates/
            └── index.html   # HTML dashboard frontend
```

---

## ⚡ Setup & Run

### 1. Hardware Pin Connections

#### ESP32 Flood Node:
- **Ultrasonic (HC-SR04)**: VCC ➔ 5V, GND ➔ GND, Trig ➔ GPIO 12, Echo ➔ GPIO 13
- **Rain Sensor**: VCC ➔ 3.3V, GND ➔ GND, AO ➔ GPIO 34
- **DHT11**: VCC ➔ 3.3V, GND ➔ GND, Data ➔ GPIO 4
- **LoRa (SX1278)**: VCC ➔ 3.3V, GND ➔ GND, NSS ➔ GPIO 5, RST ➔ GPIO 14, DIO0 ➔ GPIO 2, SCK ➔ GPIO 18, MISO ➔ GPIO 19, MOSI ➔ GPIO 23

#### ESP32 Fire Node:
- **MQ-2 Smoke Sensor**: VCC ➔ 5V, GND ➔ GND, AO ➔ GPIO 34
- **Flame Sensor**: VCC ➔ 3.3V, GND ➔ GND, DO ➔ GPIO 35
- **DHT11**: VCC ➔ 3.3V, GND ➔ GND, Data ➔ GPIO 4
- **LoRa (SX1278)**: VCC ➔ 3.3V, GND ➔ GND, NSS ➔ GPIO 5, RST ➔ GPIO 14, DIO0 ➔ GPIO 2, SCK ➔ GPIO 18, MISO ➔ GPIO 19, MOSI ➔ GPIO 23

#### Raspberry Pi Central Hub:
- **LoRa Receiver (SPI)**: Connects to SPI pins of RPi. Or, if using serial LoRa (e.g. RYLR896/EBYTE), connect TX/RX to RPi UART.
- **I2C LCD (16x2)**: VCC ➔ 5V, GND ➔ GND, SDA ➔ GPIO 2 (SDA), SCL ➔ GPIO 3 (SCL)
- **LEDs**:
  - Green (Normal) ➔ GPIO 17
  - Yellow (Warning) ➔ GPIO 27
  - Red (High/Critical) ➔ GPIO 22
- **Buzzer**: ➔ GPIO 18 (PWM)

---

### 2. Software Installation (Raspberry Pi / Dev machine)

1. Clone this repository locally.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Generate and train the initial Edge-AI risk model:
   ```bash
   python raspberry_pi/train_model.py
   ```
4. Start the Central Hub software (runs in simulation mode if not on Raspberry Pi hardware):
   ```bash
   python raspberry_pi/main.py
   ```
5. Launch the local offline Web Dashboard:
   ```bash
   python raspberry_pi/dashboard/app.py
   ```
   Open `http://localhost:5000` to view the beautiful visualization interface.
