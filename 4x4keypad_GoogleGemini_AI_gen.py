import RPi.GPIO as GPIO
import time

""" https://www.digikey.com/en/maker/tutorials/2021/how-to-connect-a-keypad-to-a-raspberry-pi

https://www.digikey.com/en/products/detail/parallax-inc/27899/27899PAR-ND/3523678
 """
# --- Configuration ---
# BCM Pin Mapping
COLS = [2, 3, 4, 17]    # OUTPUTS
ROWS = [10, 9, 11, 5]   # INPUTS

# Keypad Layout
keys = [
    ['1','2','3','A'],
    ['4','5','6','B'],
    ['7','8','9','C'],
    ['*','0','#','D']
]

# --- Setup ---
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Set rows as inputs with pull-down resistors (default LOW)
for pin in ROWS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Set columns as outputs, default LOW
for pin in COLS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# --- Main Loop ---
print("Press keypad buttons (Ctrl+C to exit)...")

try:
    while True:
        for col_index, col_pin in enumerate(COLS):
            # Activate column
            GPIO.output(col_pin, GPIO.HIGH)
            
            for row_index, row_pin in enumerate(ROWS):
                # Check if row is high
                if GPIO.input(row_pin) == GPIO.HIGH:
                    print(f"Key Pressed: {keys[row_index][col_index]}")
                    
                    # Wait for button release to avoid multiple readings
                    while GPIO.input(row_pin) == GPIO.HIGH:
                        time.sleep(0.1)
            
            # Deactivate column
            GPIO.output(col_pin, GPIO.LOW)
            
except KeyboardInterrupt:
    print("\nExiting...")
    GPIO.cleanup()
