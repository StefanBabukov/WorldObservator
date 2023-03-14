import RPi.GPIO as GPIO
import time
import threading

MEASUREMENTS = [{    "trigger": 7,    "echo": 11,    "output": 37},{    "trigger": 8,    "echo": 10,    "output": 38,},{    "trigger": 12,    "echo": 16,    "output": 40,}]

# following the board pin numbering 
GPIO.setmode(GPIO.BOARD)

#set GPIO direction (IN / OUT)
for setup in MEASUREMENTS:
    GPIO.setup(setup["trigger"], GPIO.OUT)
    GPIO.setup(setup["echo"], GPIO.IN)
    GPIO.setup(setup["output"], GPIO.OUT)

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

def alert_user(sensor, current_distance):
    if current_distance and current_distance > 70:
        return
    blink_frequency = current_distance / 100
    GPIO.output(sensor["output"], True)
    time.sleep(blink_frequency)
    GPIO.output(sensor["output"], False)
    time.sleep(blink_frequency)

def output_distance():
    while True:
        for sensor in MEASUREMENTS:
            current_distance = get_distance(sensor["trigger"], sensor["echo"])
            alert_user(sensor, current_distance)
        print("Distance 1: ", MEASUREMENTS[0]["distance"], " Distance 2: ", MEASUREMENTS[1]["distance"], " Distance 3: ", MEASUREMENTS[2]["distance"])

try:
    measuring_thread = threading.Thread(target=output_distance)
    measuring_thread.start()

    measuring_thread.join()
except KeyboardInterrupt:
    print("Measurement stopped by User")
finally:
    print("Clean up")
    GPIO.cleanup()
