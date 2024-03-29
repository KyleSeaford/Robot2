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
    
    # saw motor 
    # change pin to gpio pin number
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setup(pin, GPIO.OUT)
    
    # hammer motor
    # change pin to gpio pin number
    GPIO.setup(pin, GPIO.OUT)
    GPIO.setup(pin, GPIO.OUT)

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# led pins
LED_PIN_A = 13 
GPIO.setup(LED_PIN_A, GPIO.OUT)
LED_PIN_B = 3
GPIO.setup(LED_PIN_B, GPIO.OUT)

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

        time.sleep(1)

    # flashes blue 4 times, time to turn on controller 
    for i in range(5):
        GPIO.output(LED_PIN_A, GPIO.HIGH)
        
        time.sleep(0.5)

        GPIO.output(LED_PIN_A, GPIO.LOW)
        time.sleep(0.5) # change back to 4

    # Flash the LEDs 3 times quickly to show its ready
    for i in range(3):
        GPIO.output(LED_PIN_A, GPIO.HIGH)
        GPIO.output(LED_PIN_B, GPIO.HIGH)   
        time.sleep(0.5)
        GPIO.output(LED_PIN_A, GPIO.LOW)
        GPIO.output(LED_PIN_B, GPIO.LOW)
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

# flash red to say controllers its connected 
GPIO.output(LED_PIN_B, GPIO.HIGH) 
time.sleep(0.5)  
GPIO.output(LED_PIN_B, GPIO.LOW)

# movement motors 
# Global variables to control motor state and threads
running_left = False
running_right = False
running_reverse = False
running_hammer = False 
thread_left = None
thread_right = None
thread_reverse = None
thread_hammer = None 

def rightFORWARD():
    global running_right
    setUP()
    while running_right:  # Keep running while the button is held down
        # Right motor forward
        GPIO.output(17, False)
        GPIO.output(22, True)

def leftFORWARD():
    global running_left
    setUP()
    while running_left:  # Keep running while the button is held down
        # Left motor forward
        GPIO.output(23, False) 
        GPIO.output(24, True)

def stopMotors():
    # Stop all motors
    setUP()
    GPIO.output(17, False)
    GPIO.output(22, False)

    GPIO.output(23, False)
    GPIO.output(24, False)
    
    # change pin too gpio pin 
    GPIO.output(pin, False)
    GPIO.output(pin, False)

def reverseMotes():
    global running_reverse
    setUP()
    while running_left:  # Keep running while the button is held down
        # all motes in reverse 
        GPIO.output(17, True)
        GPIO.output(22, False)

        GPIO.output(23, True)
        GPIO.output(24, False)

# death zone
def sawOn(): 
    setUP()
    # change pin too gpio pin 
    GPIO.output(pin, False)
    GPIO.output(pin, True)

def hammer():
    setUp()
    #change pin too gpio pin 
    GPIO.output(pin, False)
    GPIO.output(pin, True)

    
for event in device.read_loop():
    if event.type == ecodes.EV_KEY:
        print('key event at {}, {}, {}'.format(
            event.timestamp(), event.code, 'down' if event.value else 'up'))  
        
        # left motors forward
        if event.code == 311:  # BTN_TL
            if event.value == 1:  # Button press
                setUP()
                # Start left motor
                GPIO.output(23, False) 
                GPIO.output(24, True)
            elif event.value == 0:  # Button release
                setUP()
                # Stop left motor
                GPIO.output(23, False)
                GPIO.output(24, False)

        # right motors forward
        if event.code == 310:  # BTN_TR
            if event.value == 1:  # Button press
                setUP()
                # Start right motor
                GPIO.output(17, False)
                GPIO.output(22, True)
            elif event.value == 0:  # Button release
                setUP()
                # Stop right motor
                GPIO.output(17, False)
                GPIO.output(22, False)

        # all motors reverse
        if event.code == 299:  # BTN_A
            if event.value == 1:  # Button press
                reverseMotes()
            elif event.value == 0:  # Button release
                stopMotors()

        # SHUT DOWN EVERYTHING, XBOX button    
        elif event.code == 172:  # xbox button
            stopMotors()
            for i in range(10): # change back to 100 
                GPIO.output(LED_PIN_B, GPIO.HIGH)
                time.sleep(0.3)
                GPIO.output(LED_PIN_B, GPIO.LOW)
                time.sleep(0.3)

            #GPIO.cleanup()
            continue 
