# 02 System Architecture

## 1. High-Level Diagram

```text
+-----------------------+           +-----------------------+
|  ESP32 Node 1: Flood  |           |  ESP32 Node 2: Fire   |
|  - Ultrasonic Sensor  |           |  - MQ-2 Smoke Sensor  |
|  - Rain Sensor        |           |  - Flame Sensor       |
|  - DHT11 Temp/Hum     |           |  - DHT11 Temp/Hum     |
+-----------+-----------+           +-----------+-----------+
            |                                   |
            | (LoRa TX)                         | (LoRa TX)
            v                                   v
    +-------+-----------------------------------+-------+
    |                    Air / Space                    |
    +-----------------------+---------------------------+
                            |
                            | (LoRa RX)
                            v
            +---------------+---------------+
            |    Raspberry Pi 4 Model B     |
            |  - UART/SPI LoRa Receiver     |
            |  - SQLite Local Database      |
            |  - Edge-AI Inference Engine   |
            |  - Flask Offline Dashboard    |
            +---------------+---------------+
                            |
            +---------------+---------------+
            |  Local Warnings & Indicators  |
            |  - 16x2 I2C LCD Status Screen |
            |  - RGB/Multicolor Alert LEDs  |
            |  - High-Decibel Buzzer Alarm  |
            +-------------------------------+
```

## 2. Component Descriptions

### A. ESP32 Sensor Nodes
Low-power microcontrollers programmed in C++/Arduino that acquire environmental data, format them into structs, and transmit them periodically using LoRa modules.

### B. Wireless Communication Link
Utilizes LoRa (Long Range) point-to-point modules working on the sub-GHz spectrum (typically 433 MHz or 868/915 MHz). Requires no Wi-Fi or cellular base stations.

### C. Raspberry Pi Edge AI Hub
Acts as the central network coordinator. It:
1. Receives and decodes radio frames from the LoRa modules.
2. Saves entries in a local SQLite database for historical record-keeping.
3. Passes the validated data to local pre-trained ML models.
4. Dictates visual and audio warnings via GPIO pins.
5. Runs a Flask web server to host a local status panel.
