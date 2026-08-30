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
        """Reads a packet from LoRa serial interface. Returns unpacked dict or None."""
        if not self.simulation_mode and self.serial_conn:
            try:
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
        return None

if __name__ == "__main__":
    receiver = LoRaReceiver()
    print("Starting simulated receiver test loop...")
    for _ in range(5):
        data = receiver.receive_packet()
        print("Received:", data)
