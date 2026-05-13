import RPi.GPIO as GPIO
import time
import serial
import sys

# ========================= CONFIGURATION =========================
# 6 Rows (outputs) and 11 Columns (inputs with pull-ups)
ROW_PINS = [17, 18, 27, 22, 23, 24]      # BCM numbering - adjust as needed
COL_PINS = [5, 6, 13, 19, 26, 12, 16, 20, 21, 25, 7]  # 11 columns

# Serial output at 9600 baud (UART0 on /dev/serial0 or /dev/ttyS0)
SERIAL_PORT = '/dev/serial0'  # or '/dev/ttyAMA0' / '/dev/ttyS0'
BAUD_RATE = 9600

# Debounce time (ms)
DEBOUNCE_MS = 20

# Simple key mapping: row * cols + col  (0-65)
# You can customize this for MIDI notes or your synth mapping
def get_key_id(row, col):
    return row * 11 + col

# ================================================================

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Rows as outputs (initially HIGH)
for row in ROW_PINS:
    GPIO.setup(row, GPIO.OUT)
    GPIO.output(row, GPIO.HIGH)

# Columns as inputs with pull-up resistors
for col in COL_PINS:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Open serial port
try:
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Serial opened on {SERIAL_PORT} at {BAUD_RATE} baud")
except Exception as e:
    print(f"Failed to open serial: {e}")
    print("Continuing without serial output...")
    ser = None

# State tracking for debouncing and change detection
last_state = [[False for _ in range(11)] for _ in range(6)]
debounce_timer = [[0 for _ in range(11)] for _ in range(6)]

print("6x11 Keyboard Matrix Scanner started. Press Ctrl+C to exit.")

try:
    while True:
        current_time = time.time() * 1000
        
        for r in range(6):
            # Activate current row (set LOW)
            GPIO.output(ROW_PINS[r], GPIO.LOW)
            time.sleep(0.001)  # Small settle time
            
            for c in range(11):
                key_pressed = not GPIO.input(COL_PINS[c])  # LOW = pressed
                key_id = get_key_id(r, c)
                
                # Debounce
                if key_pressed != last_state[r][c]:
                    if current_time - debounce_timer[r][c] > DEBOUNCE_MS:
                        last_state[r][c] = key_pressed
                        debounce_timer[r][c] = current_time
                        
                        if key_pressed:
                            event = f"KEYON:{key_id}\n"
                            print(f"Key {key_id} (r{r}c{c}) ON")
                        else:
                            event = f"KEYOFF:{key_id}\n"
                            print(f"Key {key_id} (r{r}c{c}) OFF")
                        
                        # Send over serial
                        if ser and ser.is_open:
                            try:
                                ser.write(event.encode('utf-8'))
                            except:
                                pass
                else:
                    # Reset debounce timer when stable
                    debounce_timer[r][c] = current_time
        
            # Deactivate row (set HIGH)
            GPIO.output(ROW_PINS[r], GPIO.HIGH)
        
        time.sleep(0.005)  # ~200 Hz scan rate - fast enough for organ feel

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    if ser and ser.is_open:
        ser.close()
    GPIO.cleanup()
