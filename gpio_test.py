import RPi.GPIO as GPIO
import time

# use P1 header pin numbering convention
GPIO.setmode(GPIO.BCM)

# Set up the GPIO channels - one input and one output
GPIO.setup(20, GPIO.OUT)

# Output to pin 40 / GPIO 21
GPIO.output(20, GPIO.LOW)
GPIO.output(20, GPIO.HIGH)
time.sleep(2)
GPIO.cleanup()
