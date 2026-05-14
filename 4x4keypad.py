import RPi.GPIO as GPIO
import time

# GPIO Pin Setup (BCM Numbering)
ROWS = [25, 8, 7, 1]
COLS = [12, 16, 20, 21]

# Keypad Layout
KEYS = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

def setup():
    GPIO.setmode(GPIO.BCM)
    # Set rows as outputs, initialized to LOW
    for r in ROWS:
        GPIO.setup(r, GPIO.OUT)
        GPIO.output(r, GPIO.LOW)
    # Set columns as inputs with internal pull-down resistors
    for c in COLS:
        GPIO.setup(c, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def scan_keypad():
    for row_idx, row_pin in enumerate(ROWS):
        # Send a HIGH pulse to the current row
        GPIO.output(row_pin, GPIO.HIGH)
        for col_idx, col_pin in enumerate(COLS):
            # Check if any column in this row is now HIGH
            if GPIO.input(col_pin) == GPIO.HIGH:
                key = KEYS[row_idx][col_idx]
                print(f"Key Pressed: {key}")
                # Wait until button is released to avoid double-triggers
                while GPIO.input(col_pin) == GPIO.HIGH:
                    time.sleep(0.05)
                GPIO.output(row_pin, GPIO.LOW)
                return key
        # Reset row to LOW before moving to next
        GPIO.output(row_pin, GPIO.LOW)
    return None

try:
    setup()
    print("Keypad scanner active. Press CTRL+C to exit.")
    while True:
        scan_keypad()
        time.sleep(0.1)  # Polling interval
except KeyboardInterrupt:
    GPIO.cleanup()
