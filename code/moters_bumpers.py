from evdev import InputDevice, list_devices, categorize, ecodes, KeyEvent
import time
from threading import Thread

import RPi.GPIO as GPIO


# Global variable to control motor state
running = False

def setUP():
    # Set up the GPIO pins
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Set up the GPIO pins as outputs

    # Right motor
    GPIO.setup(17, GPIO.OUT)
    GPIO.setup(22, GPIO.OUT)

    # Left motor 
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# led pins
LED_PIN_A = 13 
GPIO.setup(LED_PIN_A, GPIO.OUT)
LED_PIN_B = 3
GPIO.setup(LED_PIN_B, GPIO.OUT)

def rightFORWARD():
    global running
    setUP()
    # Right motor forward
    GPIO.output(17, False)
    GPIO.output(22, True)
    # Left motor off
    GPIO.output(23, False) 
    GPIO.output(24, False)


def rightBACK():
    global running
    setUP()
    # Right motor backward
    GPIO.output(17, True)
    GPIO.output(22, False)
    # Left motor off
    GPIO.output(23, False) 
    GPIO.output(24, False)

def leftFORWARD():
    global running    
    setUP()
    # Right motor off
    GPIO.output(17, False)
    GPIO.output(22, False)
    # Left motor backward
    GPIO.output(23, False) 
    GPIO.output(24, True)

def leftBACK():
    global running
    setUP()
    # Right motor off
    GPIO.output(17, False)
    GPIO.output(22, False)
    # left motors backwards
    GPIO.output(23, True) 
    GPIO.output(24, False)

    
def Start_delay():
    # delay while the controller is turned on
    # Flash the LEDs every 5 seconds for 25 seconds
    
    # flashes all 2, once to tell its on 
    for i in range(1):
        GPIO.output(LED_PIN_A, GPIO.HIGH)
        GPIO.output(LED_PIN_B, GPIO.HIGH)

        time.sleep(1)

        GPIO.output(LED_PIN_A, GPIO.LOW)
        GPIO.output(LED_PIN_B, GPIO.LOW)

        time.sleep(2) # change back to 4

    # flashes blue 4 times, time to turn on controller 
    time.sleep(1)
    for i in range(4):
        GPIO.output(LED_PIN_A, GPIO.HIGH)
        time.sleep(1)

        GPIO.output(LED_PIN_A, GPIO.LOW)
        time.sleep(4) # change back to 4

    # Flash the LEDs 3 times quickly to show its ready
    for i in range(3):
        GPIO.output(LED_PIN_A, GPIO.HIGH)
        GPIO.output(LED_PIN_B, GPIO.HIGH)   
        time.sleep(0.5)
        GPIO.output(LED_PIN_A, GPIO.LOW)
        GPIO.output(LED_PIN_B, GPIO.LOW)
        time.sleep(0.5)

# Start_delay()

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

# flash red to say controllers its connected 
GPIO.output(LED_PIN_B, GPIO.HIGH) 
time.sleep(0.5)  
GPIO.output(LED_PIN_B, GPIO.LOW)

for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        keyevent = categorize(event)
        print('key event at {}, {} ({}), {}'.format(
            event.timestamp(), event.code, keyevent.keycode[0], 'down' if event.value else 'up'))  
        
        if keyevent.keycode[0] == 'B':
            if keyevent.keystate == 1:  # Button press
                running = True
                Thread(target=leftFORWARD).start()  # Start motor in a new thread
            elif keyevent.keystate == 0:  # Button release
                running = False  # Stop the motor

        elif keyevent.keycode[0] == 'BTN_TR':
            if keyevent.keystate == 1:  # Button press
                running = True
                Thread(target=rightFORWARD).start()  # Start motor in a new thread
            elif keyevent.keystate == 0:  # Button release
                running = False  # Stop the motor

        # SHUT DOWN EVERYTHING, XBOX button    
        elif keyevent.keycode[0] == 'K':
            GPIO.output(LED_PIN_B, GPIO.HIGH)
            time.sleep(1)
            GPIO.output(LED_PIN_B, GPIO.LOW)
            GPIO.cleanup()
            break