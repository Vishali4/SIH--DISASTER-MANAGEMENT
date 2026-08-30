import time
import sys

# Hardware Pin Definitions
GREEN_LED = 17
YELLOW_LED = 27
RED_LED = 22
BUZZER_PIN = 18

PI_HARDWARE_AVAILABLE = False
try:
    import RPi.GPIO as GPIO
    import smbus
    PI_HARDWARE_AVAILABLE = True
except ImportError:
    pass

class LCDMock:
    def lcd_init(self): pass
    def lcd_display_string(self, string, line):
        print(f"[LCD Mock] Line {line}: {string}")
    def lcd_clear(self): pass

# Actual working PCF8574 I2C 1602 LCD Driver
class I2CLCDDriver:
    def __init__(self, address=0x27):
        self.address = address
        self.mock = False
        if PI_HARDWARE_AVAILABLE:
            try:
                self.bus = smbus.SMBus(1)
                self.lcd_write(0x33) # Initialize
                self.lcd_write(0x32) # Set to 4-bit mode
                self.lcd_write(0x28) # 2 line, 5x7 matrix
                self.lcd_write(0x0C) # Display on, cursor off
                self.lcd_write(0x06) # Increment cursor
                self.lcd_write(0x01) # Clear display
                time.sleep(0.005)
            except Exception as e:
                print(f"Failed to initialize actual I2C LCD: {e}. Using mock.")
                self.mock = True
                self.lcd = LCDMock()
        else:
            self.mock = True
            self.lcd = LCDMock()

    def write_cmd(self, cmd):
        self.bus.write_byte(self.address, cmd)

    def lcd_write(self, cmd, mode=0):
        # mode: 0 for command, 1 for data
        backlight = 0x08  # 0x08 is Backlight ON, 0x00 is Backlight OFF
        high_nibble = (cmd & 0xF0) | backlight | mode
        low_nibble = ((cmd << 4) & 0xF0) | backlight | mode
        
        # Write high nibble
        self.write_cmd(high_nibble | 0x04) # EN High
        time.sleep(0.0005)
        self.write_cmd(high_nibble & ~0x04) # EN Low
        time.sleep(0.0001)
        
        # Write low nibble
        self.write_cmd(low_nibble | 0x04) # EN High
        time.sleep(0.0005)
        self.write_cmd(low_nibble & ~0x04) # EN Low
        time.sleep(0.0001)

    def lcd_display_string(self, string, line):
        if self.mock:
            self.lcd.lcd_display_string(string, line)
            return
            
        # Select LCD line position
        if line == 1:
            self.lcd_write(0x80)
        elif line == 2:
            self.lcd_write(0xC0)
            
        # Print string characters
        for char in string[:16]:
            self.lcd_write(ord(char), 1)

    def lcd_clear(self):
        if self.mock:
            self.lcd.lcd_clear()
            return
        self.lcd_write(0x01)
        time.sleep(0.005)

class HardwareController:
    def __init__(self):
        self.current_risk = "NORMAL"
        self.lcd = I2CLCDDriver()
        
        if PI_HARDWARE_AVAILABLE:
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            GPIO.setup(GREEN_LED, GPIO.OUT)
            GPIO.setup(YELLOW_LED, GPIO.OUT)
            GPIO.setup(RED_LED, GPIO.OUT)
            GPIO.setup(BUZZER_PIN, GPIO.OUT)
            self.pwm = GPIO.PWM(BUZZER_PIN, 1000) # 1kHz
            self.pwm.start(0)
            print("RPi GPIO Hardware controller initialized.")
        else:
            print("Running in hardware simulation mode (no actual Pi GPIO found).")

    def set_alert_level(self, risk_level):
        """Sets the LED and buzzer alert levels based on risk."""
        self.current_risk = risk_level.upper()
        
        if PI_HARDWARE_AVAILABLE:
            # Clear all LEDs first
            GPIO.output(GREEN_LED, GPIO.LOW)
            GPIO.output(YELLOW_LED, GPIO.LOW)
            GPIO.output(RED_LED, GPIO.LOW)
            self.pwm.ChangeDutyCycle(0)
            
            if self.current_risk == "NORMAL":
                GPIO.output(GREEN_LED, GPIO.HIGH)
            elif self.current_risk == "WARNING":
                GPIO.output(YELLOW_LED, GPIO.HIGH)
                # Intermittent buzzer
                self.pwm.ChangeFrequency(1000)
                self.pwm.ChangeDutyCycle(10)
                time.sleep(0.1)
                self.pwm.ChangeDutyCycle(0)
            elif self.current_risk == "HIGH":
                GPIO.output(RED_LED, GPIO.HIGH)
                # Faster intermittent buzzer
                self.pwm.ChangeFrequency(1500)
                self.pwm.ChangeDutyCycle(30)
                time.sleep(0.05)
                self.pwm.ChangeDutyCycle(0)
            elif self.current_risk == "CRITICAL":
                GPIO.output(RED_LED, GPIO.HIGH)
                # Continuous alarm
                self.pwm.ChangeFrequency(2000)
                self.pwm.ChangeDutyCycle(50)
        else:
            # Console simulation output
            print(f"[ALERT STATE] -> {self.current_risk}")
            if self.current_risk == "NORMAL":
                print("  [Green LED: ON]  [Yellow LED: OFF] [Red LED: OFF] [Buzzer: OFF]")
            elif self.current_risk == "WARNING":
                print("  [Green LED: OFF] [Yellow LED: ON]  [Red LED: OFF] [Buzzer: INTERMITTENT]")
            elif self.current_risk == "HIGH":
                print("  [Green LED: OFF] [Yellow LED: OFF] [Red LED: ON]  [Buzzer: FAST]")
            elif self.current_risk == "CRITICAL":
                print("  [Green LED: OFF] [Yellow LED: OFF] [Red LED: ON]  [Buzzer: CONTINUOUS ALARM]")

    def display_status(self, line1, line2):
        """Displays status messages on the LCD screen."""
        self.lcd.lcd_clear()
        self.lcd.lcd_display_string(line1[:16], 1)
        self.lcd.lcd_display_string(line2[:16], 2)

    def cleanup(self):
        if PI_HARDWARE_AVAILABLE:
            self.pwm.stop()
            GPIO.cleanup()
            print("GPIO Cleanup complete.")

if __name__ == "__main__":
    controller = HardwareController()
    try:
        print("Testing alerting levels...")
        controller.display_status("SIH Node Test", "Status: OK")
        for level in ["NORMAL", "WARNING", "HIGH", "CRITICAL"]:
            controller.set_alert_level(level)
            time.sleep(1)
    finally:
        controller.cleanup()
