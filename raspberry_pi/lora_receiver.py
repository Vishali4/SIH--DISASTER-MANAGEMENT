import time
import struct
import random

SERIAL_PORT_AVAILABLE = False
try:
    import serial
    SERIAL_PORT_AVAILABLE = True
except ImportError:
    pass

class LoRaReceiver:
    def __init__(self, port="/dev/ttyAMA0", baudrate=115200, timeout=1.0):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = None
        self.simulation_mode = True

        if SERIAL_PORT_AVAILABLE:
            try:
                self.serial_conn = serial.Serial(
                    port=self.port,
                    baudrate=self.baudrate,
                    timeout=self.timeout
                )
                self.simulation_mode = False
                print(f"Connected to actual LoRa hardware on port {port}")
            except Exception as e:
                print(f"Failed to open serial port {port}: {e}. Starting in Simulation Mode.")
        else:
            print("pyserial package not available or failed. Starting in Simulation Mode.")

    def receive_packet(self):
        """Reads a packet from LoRa. If no packet is received within 3 seconds, returns simulated data."""
        # 1. Try reading real serial hardware data
        if not self.simulation_mode and self.serial_conn:
            try:
                # Set a non-blocking check
                if self.serial_conn.in_waiting > 0:
                    line = self.serial_conn.readline().decode('utf-8', errors='ignore').strip()
                    if line.startswith("DATA:"):
                        parts = line.split(":")[1].split(",")
                        node_id = int(parts[0])
                        packet_id = int(parts[1])
                        temp = float(parts[2])
                        hum = float(parts[3])
                        val1 = float(parts[4])
                        val2 = int(parts[5])
                        
                        if node_id == 1:
                            return {
                                "node_id": node_id,
                                "packet_id": packet_id,
                                "temperature": temp,
                                "humidity": hum,
                                "water_distance": val1,
                                "rain_value": val2
                            }
                        elif node_id == 2:
                            return {
                                "node_id": node_id,
                                "packet_id": packet_id,
                                "temperature": temp,
                                "humidity": hum,
                                "smoke_value": int(val1),
                                "flame_detected": val2
                            }
            except Exception as e:
                print(f"Error reading from serial: {e}")

        # 2. Simulation / Dummy Data Fallback (triggers every 3 seconds if no real data arrived)
        time.sleep(3)
        node_id = random.choice([1, 2])
        packet_id = random.randint(1000, 9999)
        temp = round(random.uniform(22.0, 48.0), 2)
        hum = round(random.uniform(15.0, 95.0), 2)
        
        if node_id == 1:
            # Flood Node simulation data
            state = random.choice(["normal", "rainy", "flooding", "critical_flood"])
            if state == "normal":
                water_distance = round(random.uniform(110.0, 180.0), 2)
                rain_val = random.randint(3000, 4095)
            elif state == "rainy":
                water_distance = round(random.uniform(80.0, 110.0), 2)
                rain_val = random.randint(1000, 2000)
            elif state == "flooding":
                water_distance = round(random.uniform(40.0, 75.0), 2)
                rain_val = random.randint(400, 1200)
            else:  # critical_flood
                water_distance = round(random.uniform(10.0, 35.0), 2)
                rain_val = random.randint(100, 500)
                
            return {
                "node_id": node_id,
                "packet_id": packet_id,
                "temperature": temp,
                "humidity": hum,
                "water_distance": water_distance,
                "rain_value": rain_val
            }
        else:
            # Fire Node simulation data
            state = random.choice(["normal", "smoky", "fire", "critical_fire"])
            if state == "normal":
                smoke_val = random.randint(100, 500)
                flame_detected = 0
            elif state == "smoky":
                smoke_val = random.randint(600, 1200)
                flame_detected = 0
            elif state == "fire":
                smoke_val = random.randint(1300, 2200)
                flame_detected = 1
            else: # critical_fire
                smoke_val = random.randint(2300, 4000)
                flame_detected = 1
                
            return {
                "node_id": node_id,
                "packet_id": packet_id,
                "temperature": temp,
                "humidity": hum,
                "smoke_value": smoke_val,
                "flame_detected": flame_detected
            }

if __name__ == "__main__":
    receiver = LoRaReceiver()
    print("Starting simulated receiver test loop...")
    for _ in range(5):
        data = receiver.receive_packet()
        print("Received:", data)
