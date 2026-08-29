/**
 * ESP32 Forest-Fire/Gas Monitoring Sensor Node (Node 1)
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

#define MQ2_PIN           34    // Analog input for smoke/gas level (ADC1_CH6)
#define FLAME_PIN         35    // Digital input for flame sensor (Active LOW)

#define LORA_SS           5
#define LORA_RST          14
#define LORA_DIO0         2

// --- Node Identifier ---
const byte NODE_ID = 0x01;      // Configured as Node 1 (Fire/Gas Node)

// --- Threshold Definitions (From Specifications) ---
// MQ-2 Smoke/Gas Analog Value
#define MQ2_NORMAL_MAX    1200
#define MQ2_WARNING_MAX   1800
#define MQ2_HIGH_MAX      2500

// Temperature Thresholds (DHT11 in °C)
#define TEMP_NORMAL_MAX   35.0
#define TEMP_WARNING_MAX  40.0
#define TEMP_HIGH_MAX     45.0

// Humidity Thresholds (DHT11 in %)
#define HUM_NORMAL_MIN    40.0
#define HUM_WARNING_MIN   30.0
#define HUM_HIGH_MIN      20.0

// --- Threat Levels ---
enum ThreatLevel {
  NORMAL = 0,
  WARNING = 1,
  HIGH_RISK = 2,
  CRITICAL = 3
};

const char* threatLevelNames[] = {
  "NORMAL",
  "WARNING",
  "HIGH RISK",
  "CRITICAL"
};

// --- Global Variables ---
DHT dht(DHTPIN, DHTTYPE);
unsigned long lastTxTime = 0;
const unsigned long txInterval = 5000; // Transmit every 5 seconds
int packetCounter = 0;

// Historical values to determine trend (increasing/rising)
float prevTemp = -1.0;
int prevSmoke = -1;

// Structure to pack sensor data efficiently for LoRa transmission
struct FireDataPacket {
  byte nodeId;
  unsigned long packetId;
  float temperature;
  float humidity;
  int smokeValue;
  int flameDetected;  // 1 = Flame detected, 0 = No Flame
  byte threatLevel;    // 0 = NORMAL, 1 = WARNING, 2 = HIGH, 3 = CRITICAL
};

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("==========================================");
  Serial.println("SIH Forest-Fire/Gas Node (ESP32 #1) Starting...");
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
  Serial.println("Node 1 ready to monitor and transmit.");
}

void loop() {
  if (millis() - lastTxTime >= txInterval) {
    lastTxTime = millis();
    packetCounter++;

    // 1. Read DHT11 Temperature & Humidity
    float temp = dht.readTemperature();
    float hum = dht.readHumidity();
    
    // Check if readings failed, fallback to 0.0
    if (isnan(temp)) temp = 0.0;
    if (isnan(hum)) hum = 0.0;

    // 2. Read MQ-2 Smoke Level
    int smokeVal = analogRead(MQ2_PIN);

    // 3. Read Flame Sensor (Usually Active LOW on standard boards)
    int flameState = digitalRead(FLAME_PIN);
    bool flameDetected = (flameState == LOW); // LOW = Flame detected, HIGH = Normal

    // 4. Trend checks (Increasing/Rising)
    bool tempRising = (prevTemp >= 0.0) && (temp > prevTemp + 0.2);     // +0.2C tolerance
    bool smokeIncreasing = (prevSmoke >= 0) && (smokeVal > prevSmoke + 50); // +50 units tolerance

    // 5. Threat Level Evaluation Logic
    ThreatLevel level = NORMAL;

    if (flameDetected && (smokeVal >= MQ2_WARNING_MAX)) {
      // IF flame detected + smoke high (High Risk or Critical Smoke) -> CRITICAL FIRE
      level = CRITICAL;
    } 
    else if ((smokeVal >= MQ2_WARNING_MAX) && (temp >= TEMP_WARNING_MAX)) {
      // IF smoke high + temperature high -> HIGH FIRE RISK
      level = HIGH_RISK;
    } 
    else if (flameDetected) {
      // Flame detected on its own is high risk
      level = HIGH_RISK;
    }
    else if ((smokeIncreasing && tempRising) || 
             (smokeVal > MQ2_NORMAL_MAX && smokeVal <= MQ2_WARNING_MAX) || 
             (temp >= TEMP_NORMAL_MAX && temp < TEMP_WARNING_MAX) ||
             (hum < HUM_NORMAL_MIN && hum >= HUM_WARNING_MIN)) {
      // IF smoke increasing + temperature rising OR warning thresholds met -> WARNING
      level = WARNING;
    } 
    else {
      // Otherwise: IF smoke normal + no flame + normal temperature -> NORMAL
      level = NORMAL;
    }

    // Save current readings for next iteration's trend calculation
    prevTemp = temp;
    prevSmoke = smokeVal;

    // 6. Pack Data Into Struct
    FireDataPacket packet;
    packet.nodeId = NODE_ID;
    packet.packetId = packetCounter;
    packet.temperature = temp;
    packet.humidity = hum;
    packet.smokeValue = smokeVal;
    packet.flameDetected = flameDetected ? 1 : 0;
    packet.threatLevel = (byte)level;

    // Print values to local Serial Monitor
    Serial.printf("[TX #%d] Temp: %.1f°C | Hum: %.1f%% | Smoke: %d | Flame: %s | Threat: %s\n", 
                  packetCounter, temp, hum, smokeVal, 
                  flameDetected ? "DETECTED!" : "None", 
                  threatLevelNames[level]);

    // 7. Transmit packet via LoRaz
    LoRa.beginPacket();
    LoRa.write((uint8_t*)&packet, sizeof(packet));
    LoRa.endPacket();

    Serial.println("Packet sent successfully!");
  }
}
