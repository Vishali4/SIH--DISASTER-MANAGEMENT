/**
 * ESP32 Forest-Fire Monitoring Sensor Node (Node 2)
 * SIH - Environmental Intelligence Early-Warning Network
 * 
 * Hardware Sensors:
 * - MQ-2 Gas/Smoke Sensor (Air quality/smoke)
 * - Infrared Flame Sensor (Flame detection)
 * - DHT11 (Temperature & Humidity)
 * - SX1278 SPI LoRa Module (LoRa Transmitter)
 */

#include <SPI.h>
#include <LoRa.h>
#include <DHT.h>

// --- Pin Definitions ---
#define DHTPIN            4
#define DHTTYPE           DHT11

#define MQ2_PIN           34    // Analog input for smoke/gas level
#define FLAME_PIN         35    // Digital/Analog input for flame (GPIO 35 input only)

#define LORA_SS           5
#define LORA_RST          14
#define LORA_DIO0         2

// --- Node Identifier ---
const byte NODE_ID = 0x02;      // Forest-Fire Node ID

// --- Global Variables ---
DHT dht(DHTPIN, DHTTYPE);
unsigned long lastTxTime = 0;
const unsigned long txInterval = 5000; // Transmit every 5 seconds
int packetCounter = 0;

// Structure to pack sensor data efficiently for LoRa transmission
struct FireDataPacket {
  byte nodeId;
  unsigned long packetId;
  float temperature;
  float humidity;
  int smokeValue;
  int flameDetected;  // 0 = Flame detected (Active Low sensor usually) or 1 = No Flame
};

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("==========================================");
  Serial.println("SIH Forest-Fire Monitoring Node (ESP32 #2) Starting...");
  Serial.println("==========================================");

  // Initialize sensors
  dht.begin();
  pinMode(MQ2_PIN, INPUT);
  pinMode(FLAME_PIN, INPUT);

  // Initialize LoRa transceiver
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  
  // Set frequency to 433MHz
  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa initialization failed! Check wiring.");
    while (1);
  }
  
  LoRa.setTxPower(17); // Set TX power
  Serial.println("LoRa Transceiver Initialized successfully @ 433 MHz");
  Serial.println("Forest-Fire Node Ready to Transmit.");
}

void loop() {
  if (millis() - lastTxTime >= txInterval) {
    lastTxTime = millis();
    packetCounter++;

    // 1. Read DHT11 Temperature & Humidity
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    
    // Check if readings failed
    if (isnan(temp)) temp = 0.0;
    if (isnan(hum)) hum = 0.0;

    // 2. Read MQ-2 Smoke Level
    int smokeVal = analogRead(MQ2_PIN);

    // 3. Read Flame Sensor
    int flameState = digitalRead(FLAME_PIN);

    // 4. Pack Data Into Struct
    FireDataPacket packet;
    packet.nodeId = NODE_ID;
    packet.packetId = packetCounter;
    packet.temperature = temp;
    packet.humidity = hum;
    packet.smokeValue = smokeVal;
    packet.flameDetected = (flameState == LOW) ? 1 : 0; // Standard flame modules are Active Low

    // Print values to local Serial Monitor
    Serial.printf("[TX #%d] Temp: %.1fC | Hum: %.1f%% | Smoke Val: %d | Flame: %s\n", 
                  packetCounter, temp, hum, smokeVal, (packet.flameDetected == 1) ? "DETECTED!" : "None");

    // 5. Transmit packet via LoRa
    LoRa.beginPacket();
    LoRa.write((uint8_t*)&packet, sizeof(packet));
    LoRa.endPacket();

    Serial.println("Packet sent successfully!");
  }
}
