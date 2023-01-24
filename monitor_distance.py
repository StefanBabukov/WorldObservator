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

def blink_led(distance):
    while True:        
        if distance > 500:
            continue
        sleep_time = distance/100
        GPIO.output(led, True)
        time.sleep(sleep_time/2)
        GPIO.output(led, False)
        time.sleep(sleep_time/2)

def output_distance():
    while True:
        distance = get_distance()
        print("Distance: ", distance, " cm")
        blink_led_thread = threading.Thread(target=blink_led, args=(distance,))
        blink_led_thread.start()
        blink_led_thread.join()

try:
    output_thread = threading.Thread(target=output_distance)
    output_thread.start()
    output_thread.join()
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()