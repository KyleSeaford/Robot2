import RPi.GPIO as GPIO
import time

# Define constants
LED_PINS = [18, 21]  # LED pins
SLEEP_TIME = 0.1  # Time to sleep

# Set GPIO mode and warnings
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def flash_led(pin):
    # Setup the pin as output
    GPIO.setup(pin, GPIO.OUT)

    # LED on 
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(SLEEP_TIME)

    # LED off
    GPIO.output(pin, GPIO.LOW)
    time.sleep(SLEEP_TIME)

def flash():
    while True:
        for pin in LED_PINS:
            flash_led(pin)

flash()