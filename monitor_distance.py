import RPi.GPIO as GPIO
import time
import threading

GPIO_TRIGGER = 7
GPIO_ECHO = 11
led = 13

# following the board pin numbering 
GPIO.setmode(GPIO.BOARD)

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(led, GPIO.OUT)

distance = 0

def get_distance():
     
    #GPIO pins
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(GPIO_ECHO) == 0:
        start_time = time.time()

    while GPIO.input(GPIO_ECHO) == 1:
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
        distance = get_distance()
        print("Distance: ", distance, " cm")

try:
    output_thread = threading.Thread(target=output_distance)
    output_thread2 = threading.Thread(target=alert_user)

    output_thread.start()
    output_thread2.start()
    output_thread.join()
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()