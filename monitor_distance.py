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
global distance

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

def blink_led():
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

try:
    output_thread = threading.Thread(target=output_distance)
    output_thread.start()
    output_thread.join()
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()


# def distance():
#     # set Trigger to HIGH
#     GPIO.output(GPIO_TRIGGER, True)
 
#     # set Trigger after 0.01ms to LOW
#     time.sleep(0.00001)
#     GPIO.output(GPIO_TRIGGER, False)
 
#     StartTime = time.time()
#     StopTime = time.time()
 
#     # save StartTime
#     while GPIO.input(GPIO_ECHO) == 0:
#         StartTime = time.time()
 
#     # save time of arrival
#     while GPIO.input(GPIO_ECHO) == 1:
#         StopTime = time.time()
 
#     # time difference between start and arrival
#     TimeElapsed = StopTime - StartTime
#     # multiply with the sonic speed (34300 cm/s)
#     # and divide by 2, because there and back
#     distance = (TimeElapsed * 34300) / 2
 
#     return distance


# print('starting to measure')
# try:
#     while True:
#         dist = distance()
#         print ("Measured Distance = %.1f cm" % dist)
        
#         if dist > 500:
#             continue
#         sleep_time = dist/100
#         GPIO.output(led, True)
#         time.sleep(sleep_time/2)
#         GPIO.output(led, False)
#         time.sleep(sleep_time/2)
# except KeyboardInterrupt:
#     print("Measurement stopped by User")
#     GPIO.cleanup()
