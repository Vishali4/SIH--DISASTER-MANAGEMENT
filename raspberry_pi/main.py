import time
from database import init_db, log_sensor_data
from hardware_control import HardwareController
from edge_ai import EdgeAIInference
from lora_receiver import LoRaReceiver

def run_hub():
    print("==================================================")
    print("SIH Environmental Intelligence Network Hub Starting...")
    print("==================================================")

    # 1. Initialize Database
    init_db()

    # 2. Initialize Hardware Output Controller
    hardware = HardwareController()

    # 3. Initialize AI inference engine
    ai_engine = EdgeAIInference()

    # 4. Initialize LoRa Serial Receiver (with auto-detection for Windows)
    import sys
    default_port = "/dev/ttyAMA0"
    if sys.platform.startswith('win'):
        try:
            import serial.tools.list_ports
            ports = list(serial.tools.list_ports.comports())
            esp_ports = [p.device for p in ports if any(x in p.description for x in ["USB", "UART", "Silicon Labs", "CH340", "CP210"])]
            if esp_ports:
                default_port = esp_ports[0]
                print(f"Auto-detected ESP32 LoRa Gateway on Windows port: {default_port}")
            elif ports:
                default_port = ports[0].device
                print(f"Using first available serial port: {default_port}")
            else:
                default_port = "COM3"
                print(f"No serial ports found. Defaulting to: {default_port}")
        except Exception as e:
            default_port = "COM3"
            print(f"Error scanning serial ports: {e}. Defaulting to COM3")
    
    lora = LoRaReceiver(port=default_port)

    hardware.display_status("SIH Central Hub", "System: Active")
    time.sleep(2)
    hardware.display_status("Waiting for Node", "Transmissions...")

    print("\nEntering receiver & risk assessment loop. Press Ctrl+C to stop.")
    
    # Store current state for alert aggregation
    last_alerts = {"flood": "NORMAL", "fire": "NORMAL"}
    
    try:
        while True:
            packet = lora.receive_packet()
            if not packet:
                # Idle delay if no serial data in simulated/polling mode
                time.sleep(0.1)
                continue
                
            node_id = packet["node_id"]
            packet_id = packet["packet_id"]
            temp = packet["temperature"]
            hum = packet["humidity"]
            
            print(f"\n[RX Packet #{packet_id} from Node {node_id}]")
            
            risk_level = "NORMAL"
            confidence = 1.0
            
            # Flood Node
            if node_id == 1:
                water_dist = packet["water_distance"]
                rain_val = packet["rain_value"]
                
                # Perform AI Inference
                risk_level, confidence = ai_engine.evaluate_flood(
                    temp, hum, water_dist, rain_val
                )
                
                print(f"  Type: FLOOD | Dist: {water_dist}cm | Rain: {rain_val}")
                print(f"  AI Assessment: {risk_level} (Conf: {confidence:.2f})")
                
                # Log to DB
                log_sensor_data(
                    node_id=node_id,
                    packet_id=packet_id,
                    temperature=temp,
                    humidity=hum,
                    water_distance=water_dist,
                    rain_value=rain_val,
                    risk_level=risk_level,
                    confidence=confidence
                )
                
                last_alerts["flood"] = risk_level
                
            # Fire Node
            elif node_id == 2:
                smoke_val = packet["smoke_value"]
                flame_detected = packet["flame_detected"]
                
                # Perform AI Inference
                risk_level, confidence = ai_engine.evaluate_fire(
                    temp, hum, smoke_val, flame_detected
                )
                
                print(f"  Type: FIRE | Smoke: {smoke_val} | Flame: {'YES' if flame_detected == 1 else 'NO'}")
                print(f"  AI Assessment: {risk_level} (Conf: {confidence:.2f})")
                
                # Log to DB
                log_sensor_data(
                    node_id=node_id,
                    packet_id=packet_id,
                    temperature=temp,
                    humidity=hum,
                    smoke_value=smoke_val,
                    flame_detected=flame_detected,
                    risk_level=risk_level,
                    confidence=confidence
                )
                
                last_alerts["fire"] = risk_level
            
            # Aggregate risk levels for hardware alerts (highest risk takes priority)
            priority = {"NORMAL": 0, "WARNING": 1, "HIGH": 2, "CRITICAL": 3}
            highest_risk = "NORMAL"
            for alert in last_alerts.values():
                if priority[alert] > priority[highest_risk]:
                    highest_risk = alert
            
            # Update LEDs & Buzzers
            hardware.set_alert_level(highest_risk)
            
            # Update LCD Display
            lcd_line1 = f"FL:{last_alerts['flood']} FR:{last_alerts['fire']}"
            lcd_line2 = f"ALERT: {highest_risk}"
            hardware.display_status(lcd_line1, lcd_line2)

    except KeyboardInterrupt:
        print("\nExiting Hub Orchestrator...")
    finally:
        hardware.cleanup()

if __name__ == "__main__":
    run_hub()
