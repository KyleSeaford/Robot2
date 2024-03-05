import time

import RPi.GPIO as gpio

def setUP():
    # Set up the GPIO pins
    gpio.setmode(gpio.BCM)
    gpio.setwarnings(False)

    # Set up the gpio pins as outputs

    # Right motor
    gpio.setup(17, gpio.OUT)
    gpio.setup(22, gpio.OUT)

    # Left motor 
    gpio.setup(23, gpio.OUT)
    gpio.setup(24, gpio.OUT)

def forward(sec):
    setUP()
  
    gpio.output(17, True)
    gpio.output(22, False)
    # all motors forwards
    gpio.output(23, True) 
    gpio.output(24, False)

    time.sleep(sec)
    gpio.cleanup()

def reverse(sec):
    setUP()
    gpio.output(17, False)
    gpio.output(22, True)
    # all motors backwards
    gpio.output(23, False) 
    gpio.output(24, True)

    time.sleep(sec)
    gpio.cleanup()

def left(sec):
    setUP()
    # Right motor backward
    gpio.output(17, False)
    gpio.output(22, True)
    # Left motor forward
    gpio.output(23, True) 
    gpio.output(24, False)

    time.sleep(sec)
    gpio.cleanup()

def right(sec):
    setUP()
    # Right motor forward
    gpio.output(17, True)
    gpio.output(22, False)
    # Left motor backward
    gpio.output(23, False) 
    gpio.output(24, True)

    time.sleep(sec)
    gpio.cleanup()



print("forward")
forward(5)

print("reverse")
reverse(5)

print("left")
left(5)

print("right")
right(5)
