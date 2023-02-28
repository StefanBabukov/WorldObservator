import RPi.GPIO as GPIO
import time
import threading

TRIGGER = 7
ECHO = 11

TRIGGER2 = 8
ECHO2 = 10

led = 13

# following the board pin numbering 
GPIO.setmode(GPIO.BOARD)

#set GPIO direction (IN / OUT)
GPIO.setup(TRIGGER, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(TRIGGER2, GPIO.OUT)
GPIO.setup(ECHO2, GPIO.IN)
GPIO.setup(led, GPIO.OUT)

distance = 0

def get_distance(trigger, echo):
     
    #GPIO pins
    GPIO.output(trigger, True)

    time.sleep(0.00001)
    GPIO.output(trigger, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo) == 0:
        start_time = time.time()

    while GPIO.input(echo) == 1:
        stop_time = time.time()

    distance = (stop_time - start_time) * 34300 / 2
    return distance

def alert_user():
    global distance
    while True:
        if distance > 70:
            continue
        blink_frequency = distance / 100
        GPIO.output(led, True)
        time.sleep(blink_frequency)
        GPIO.output(led, False)
        time.sleep(blink_frequency)

def output_distance():
    global distance
    while True:
        distance = get_distance(TRIGGER, ECHO)
        distance2 = get_distance(TRIGGER2, ECHO2)
        print("Distance 1: ", distance, " cm", " Distance 2: ", distance2, " cm")

try:
    output_thread = threading.Thread(target=output_distance)
    output_thread2 = threading.Thread(target=alert_user)

    output_thread.start()
    output_thread2.start()
    output_thread.join()
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()