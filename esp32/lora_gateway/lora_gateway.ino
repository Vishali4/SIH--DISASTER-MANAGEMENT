/**
 * ESP32 LoRa Gateway Receiver (Connected to Laptop USB)
 * SIH - Environmental Intelligence Early-Warning Network
 * 
 * Hardware:
 * - ESP32 DevKit V1
 * - SX1278 SPI LoRa Module (LoRa Receiver)
 * 
 * Purpose:
 * Receives wireless data packets from Node 1 (Flood) and Node 2 (Fire),
 * and prints them to USB Serial in a standardized CSV string format.
 */

#include <SPI.h>
#include <LoRa.h>

// --- Pin Definitions (Same SPI layout) ---
#define LORA_SS           5
#define LORA_RST          14
#define LORA_DIO0         2

// Structures to match Transmitter Nodes
// (Aligned with 4-byte boundary padding matching default compiler options)
struct FloodDataPacket {
  byte nodeId;
  unsigned long packetId;
  float temperature;
  float humidity;
  float waterDistanceCm;
  int rainValue;       // Added to match updated transmitter structure
  byte threatLevel;
};

struct FireDataPacket {
  byte nodeId;
  unsigned long packetId;
  float temperature;
  float humidity;
  int smokeValue;
  int flameDetected;
  byte threatLevel;
};

void setup() {
  Serial.begin(115200);
  while (!Serial);

  Serial.println("==========================================");
  Serial.println("SIH LoRa-to-USB Gateway starting...");
  Serial.println("==========================================");

  // Initialize LoRa
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);
  
  if (!LoRa.begin(433E6)) {
    Serial.println("LoRa initialization failed! Check wiring.");
    while (1);
  }
  
  LoRa.setTxPower(17);
  Serial.println("LoRa Gateway Initialized successfully @ 433 MHz");
  Serial.println("Listening for sensor node transmissions...");
}

void loop() {
  int packetSize = LoRa.parsePacket();
  if (packetSize > 0) {
    // Read the first byte to identify the node
    byte nodeId = LoRa.peek();

    if (nodeId == 0x01) {
      // Node 1: Flood Node
      FloodDataPacket packet;
      int bytesRead = 0;
      byte* p = (byte*)&packet;
      
      while (LoRa.available() && bytesRead < sizeof(packet)) {
        p[bytesRead++] = LoRa.read();
      }

      // Check packet integrity and print in CSV format expected by Python
      // Format: DATA:node_id,packet_id,temp,hum,water_distance,rain_val
      Serial.printf("DATA:%d,%d,%.2f,%.2f,%.2f,%d\n", 
                    packet.nodeId, 
                    packet.packetId, 
                    packet.temperature, 
                    packet.humidity, 
                    packet.waterDistanceCm, 
                    packet.rainValue);
    } 
    else if (nodeId == 0x02) {
      // Node 2: Fire Node
      FireDataPacket packet;
      int bytesRead = 0;
      byte* p = (byte*)&packet;
      
      while (LoRa.available() && bytesRead < sizeof(packet)) {
        p[bytesRead++] = LoRa.read();
      }

      // Format: DATA:node_id,packet_id,temp,hum,smoke_value,flame_detected
      Serial.printf("DATA:%d,%d,%.2f,%.2f,%d,%d\n", 
                    packet.nodeId, 
                    packet.packetId, 
                    packet.temperature, 
                    packet.humidity, 
                    packet.smokeValue, 
                    packet.flameDetected);
    }
    else {
      // Unrecognized Node ID, discard remaining packet buffer
      while(LoRa.available()) {
        LoRa.read();
      }
    }
  }
}
