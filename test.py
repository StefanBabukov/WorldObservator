import RPi.GPIO as GPIO
import time

# Set the GPIO pin numbering mode
GPIO.setmode(GPIO.BOARD)
LED=38
# Set up the echo pins as inputs
GPIO.setup(LED, GPIO.OUT)
# 

while True:
    GPIO.output(LED, True)

# Clean up the GPIO pins
GPIO.cleanup()