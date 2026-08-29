/**
 * ESP32 Flood Monitoring Sensor Node (Node 1)
 * SIH - Environmental Intelligence Early-Warning Network
 * 
 * Hardware Sensors:
 * - HC-SR04 Waterproof Ultrasonic Sensor (Water Level)
 * - Analog Rain Sensor (Precipitation)
 * - DHT11 (Temperature & Humidity)
 * - SX1278 SPI LoRa Module (LoRa Transmitter)
 */

#include <SPI.h>
#include <LoRa.h>
#include <DHT.h>

// --- Pin Definitions ---
#define DHTPIN            4
#define DHTTYPE           DHT11

#define TRIG_PIN          12
#define ECHO_PIN          13
#define RAIN_PIN          34    // Analog input pin for rain level (ADC1_CH6)

#define LORA_SS           5
#define LORA_RST          14
#define LORA_DIO0         2

// --- Node Identifier ---
const byte NODE_ID = 0x01;      // Flood Node ID

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

// Structure to pack sensor data efficiently for LoRa transmission
struct FloodDataPacket {
  byte nodeId;
  unsigned long packetId;
  float temperature;
  float humidity;
  float waterDistanceCm;
  int rainValue;       // Analog rain reading (0-4095)
  byte threatLevel;    // 0 = NORMAL, 1 = WARNING, 2 = HIGH, 3 = CRITICAL
};

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("==========================================");
  Serial.println("SIH Flood Monitoring Node (ESP32 #1) Starting...");
  Serial.println("==========================================");

  // Initialize sensors
  dht.begin();
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(RAIN_PIN, INPUT);

  // Initialize LoRa transceiver
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  
  // Set frequency to 433MHz
  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa initialization failed! Check wiring.");
    while (1);
  }
  
  LoRa.setTxPower(17); // Set TX power
  Serial.println("LoRa Transceiver Initialized successfully @ 433 MHz");
  Serial.println("Flood Node Ready to Transmit.");
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

    // 2. Read Ultrasonic Water Level (Distance)
    float distanceCm = getUltrasonicDistance();

    // 3. Read Rain Sensor
    int rainVal = analogRead(RAIN_PIN);

    // 4. Evaluate Threat Level Logic
    ThreatLevel level = NORMAL;

    if (distanceCm > 0.0) {
      // CRITICAL: Water distance <= 20cm OR (water distance <= 35cm AND rain value < 800)
      if (distanceCm <= 20.0 || (distanceCm <= 35.0 && rainVal < 800)) {
        level = CRITICAL;
      }
      // HIGH: Water distance <= 50cm OR (water distance <= 75cm AND rain value < 1500)
      else if (distanceCm <= 50.0 || (distanceCm <= 75.0 && rainVal < 1500)) {
        level = HIGH_RISK;
      }
      // WARNING: Water distance <= 95cm OR rain value < 2000
      else if (distanceCm <= 95.0 || rainVal < 2000) {
        level = WARNING;
      }
      // NORMAL: Water distance > 95cm AND rain value >= 2000
      else {
        level = NORMAL;
      }
    } else {
      // Out of range/failed ultrasonic sensor: base risk level solely on Rain Sensor
      if (rainVal < 800) {
        level = CRITICAL;
      } else if (rainVal < 1500) {
        level = HIGH_RISK;
      } else if (rainVal < 2000) {
        level = WARNING;
      } else {
        level = NORMAL;
      }
    }

    // 5. Pack Data Into Struct
    FloodDataPacket packet;
    packet.nodeId = NODE_ID;
    packet.packetId = packetCounter;
    packet.temperature = temp;
    packet.humidity = hum;
    packet.waterDistanceCm = distanceCm;
    packet.rainValue = rainVal;
    packet.threatLevel = (byte)level;

    // Print values to local Serial Monitor
    Serial.printf("[TX #%d] Temp: %.1fC | Hum: %.1f%% | Water Dist: %.1f cm | Rain Val: %d | Threat: %s\n", 
                  packetCounter, temp, hum, distanceCm, rainVal, threatLevelNames[level]);

    // 6. Transmit packet via LoRa
    LoRa.beginPacket();
    LoRa.write((uint8_t*)&packet, sizeof(packet));
    LoRa.endPacket();

    Serial.println("Packet sent successfully!");
  }
}

/**
 * Measures water level distance by trigger/echo timing of ultrasonic waves.
 */
float getUltrasonicDistance() {
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  long duration = pulseIn(ECHO_PIN, HIGH, 30000); // 30ms timeout
  if (duration == 0) {
    return -1.0; // Out of range or failure
  }
  
  // Speed of sound is 340 m/s or 0.0343 cm/us. Distance = (time * speed) / 2
  float distance = (duration * 0.0343) / 2.0;
  return distance;
}
