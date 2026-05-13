import RPi.GPIO as GPIO
import time

# --- Configuration ---
# Set up 6 rows and 11 columns
ROW_PINS = [2, 3, 4, 17, 27, 22]    # Example BCM GPIOs
COL_PINS = [10, 9, 11, 5, 6, 13, 19, 26, 21, 20, 16] # Example BCM GPIOs
BAUD_RATE = 9600

# Initialize GPIO
GPIO.setmode(GPIO.BCM)
for pin in ROW_PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH) # Set high (inactive)

for pin in COL_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Internal Pull-up

# --- Matrix Setup ---
matrix_state = [[False for _ in range(len(COL_PINS))] for _ in range(len(ROW_PINS))]

def scan_keyboard():
    for r in range(len(ROW_PINS)):
        GPIO.output(ROW_PINS[r], GPIO.LOW) # Activate Row
        
        for c in range(len(COL_PINS)):
            new_state = GPIO.input(COL_PINS[c]) == GPIO.LOW
            
            # Detect Change
            if new_state != matrix_state[r][c]:
                matrix_state[r][c] = new_state
                note = (r * len(COL_PINS)) + c
                action = "ON" if new_state else "OFF"
                print(f"Note {note}: {action}")
                # Add MIDI sending logic here
                
        GPIO.output(ROW_PINS[r], GPIO.HIGH) # Deactivate Row

# --- Main Loop ---
try:
    while True:
        scan_keyboard()
        time.sleep(0.001) # Small delay for stability
except KeyboardInterrupt:
    GPIO.cleanup()
