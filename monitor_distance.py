import RPi.GPIO as GPIO
import time
import threading


TRIGGERS = [7, 8, 12]
ECHOS = [11, 10, 16]
OUTPUTS = [37, 38, 40]
# following the board pin numbering 
GPIO.setmode(GPIO.BOARD)

#set GPIO direction (IN / OUT)
for trigger in TRIGGERS:
    GPIO.setup(trigger, GPIO.OUT)
for echo in ECHOS:
    GPIO.setup(echo, GPIO.IN)
for output in OUTPUTS:
    GPIO.setup(output, GPIO.OUT)

distances = []

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

def alert_user(sensor):
    global distances
    while True:
        if distances[sensor] > 70:
            continue
        blink_frequency = distances[sensor] / 100
        GPIO.output(OUTPUTS[sensor], True)
        time.sleep(blink_frequency)
        GPIO.output(OUTPUTS[sensor], False)
        time.sleep(blink_frequency)

def output_distance():
    global distances
    while True:
        for sensor in range(len(TRIGGERS)-1):
            distances[sensor] = get_distance(TRIGGERS[sensor], ECHOS[sensor])
        print("Distance 1: ", distances[0], " Distance 2: ", distances[1], " Distance 3: ", distances[2])

try:
    measuring_thread = threading.Thread(target=output_distance)

    for sensor in range(len(TRIGGERS)-1):
        thread = threading.Thread(target=alert_user, args=(sensor, ))
        thread.start()

    measuring_thread.start()
    measuring_thread.join()
except KeyboardInterrupt:
    print("Measurement stopped by User")
finally:
    print("Clean up")
    GPIO.cleanup()