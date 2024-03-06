from evdev import InputDevice, list_devices, categorize, ecodes, KeyEvent
import RPi.GPIO as GPIO
import time

# Set up the GPIO pins for the LEDs
LED_PIN_A = 13  
LED_PIN_B = 21 
LED_PIN_K = 3 

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# set up the gpio pins to outputs 
GPIO.setup(LED_PIN_A, GPIO.OUT)
GPIO.setup(LED_PIN_B, GPIO.OUT)
GPIO.setup(LED_PIN_K, GPIO.OUT)

def Start_delay():
    # delay while the contoler is turned on
    # Flash the LEDs every 5 seconds for 25 seconds
    
    # flashes all 3, once to tell its on 
    for i in range(1):
        GPIO.output(LED_PIN_A, GPIO.HIGH)
        GPIO.output(LED_PIN_B, GPIO.HIGH)
        GPIO.output(LED_PIN_K, GPIO.HIGH)   

        time.sleep(1)

        GPIO.output(LED_PIN_A, GPIO.LOW)
        GPIO.output(LED_PIN_B, GPIO.LOW)
        GPIO.output(LED_PIN_K, GPIO.LOW)   

        time.sleep(1) # change back to 9

    # flashes blue 4 times, turn on controler 
    time.sleep(1)
    for i in range(4):
        GPIO.output(LED_PIN_A, GPIO.HIGH)
        GPIO.output(LED_PIN_B, GPIO.HIGH)

        time.sleep(1)

        GPIO.output(LED_PIN_A, GPIO.LOW)
        GPIO.output(LED_PIN_B, GPIO.LOW)
        time.sleep(4) # change back to 9

    # Flash the LEDs 3 times quickly
    for i in range(3):
        GPIO.output(LED_PIN_A, GPIO.HIGH)
        GPIO.output(LED_PIN_B, GPIO.HIGH)
        GPIO.output(LED_PIN_K, GPIO.HIGH)   
        time.sleep(0.5)
        GPIO.output(LED_PIN_A, GPIO.LOW)
        GPIO.output(LED_PIN_B, GPIO.LOW)
        GPIO.output(LED_PIN_K, GPIO.LOW)
        time.sleep(0.5)

Start_delay()

# Find the Xbox Controller
devices = [InputDevice(path) for path in list_devices()]
device = None

for dev in devices:
    if dev.name == "Xbox Wireless Controller":
        device = dev
        break

if device is None:
    print("Xbox Wireless Controller not found.")
    exit()

# Function to handle button presses
def handle_button(event, pin):
    if event.value == 1:  # Button press
        GPIO.output(pin, GPIO.HIGH)
    elif event.value == 0:  # Button release
        GPIO.output(pin, GPIO.LOW)

# flash red to say its connected 
GPIO.output(LED_PIN_K, GPIO.HIGH) 
time.sleep(0.5)  
GPIO.output(LED_PIN_K, GPIO.LOW)

# Main loop
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        #print('key event at {}, {} ({}), {}'.format(
        #    event.timestamp(), event.code, keyevent.keycode[0], 'down' if event.value else 'up'))  
        
        if keyevent.keycode[0] == 'BTN_A':
            handle_button(event, LED_PIN_A)

        elif keyevent.keycode[0] == 'BTN_B':
            handle_button(event, LED_PIN_B)

        elif keyevent.keycode[0] == 'BTN_WEST':
            handle_button(event, LED_PIN_A)
            handle_button(event, LED_PIN_B)
        
        elif keyevent.keycode[0] == 'BTN_NORTH':
            handle_button(event, LED_PIN_A)
            handle_button(event, LED_PIN_B)
            handle_button(event, LED_PIN_K)


        # SHUT DOWN EVREYTHING, XBOX button    
        elif keyevent.keycode[0] == 'K':
            GPIO.output(LED_PIN_K, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(LED_PIN_K, GPIO.LOW)
            break