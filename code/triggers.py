from evdev import InputDevice, list_devices, categorize, ecodes
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

# Function to handle button presses
def handle_button(event, pin):
    if event.value == 1:  # Button press
        GPIO.output(pin, GPIO.HIGH)
    elif event.value == 0:  # Button release
        GPIO.output(pin, GPIO.LOW)


devices = [InputDevice(path) for path in list_devices()]
device = None

for dev in devices:
    if dev.name == "Xbox Wireless Controller":
        device = dev
        break

if device is None:
    print("Xbox Wireless Controller not found.")
    exit()

def handle_left_trigger(event, value):
    handle_button(event, LED_PIN_B)
    print('Left trigger pressed with value {}'.format(value))

def handle_right_trigger(event, value):
    handle_button(event, LED_PIN_A)
    print('Right trigger pressed with value {}'.format(value))
    
# Main loop
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        print('key event at {}, {} ({}), {}'.format(
            event.timestamp(), event.code, keyevent.keycode, 'down' if event.value else 'up'))
    elif event.type == ecodes.EV_ABS:
        absevent = categorize(event)
        print('ABS event at {}, {} ({}), value {}'.format(
            event.timestamp(), event.code, absevent.event.code, absevent.event.value))  # Print all ABS events
        if event.code == ecodes.ABS_RX or event.code == ecodes.ABS_RY:  # Skip joystick events
            continue
        elif event.code == ecodes.ABS_LT:  # Left trigger
            handle_left_trigger(event, absevent.event.value)
        elif event.code == ecodes.ABS_RT:  # Right trigger
            handle_right_trigger(event, absevent.event.value)